####
#
# fiction-dl
# Copyright (C) (2020) Benedykt Synakiewicz <dreamcobbler@outlook.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####

#
#
#
# Imports.
#
#
#

# Application.

from fiction_dl.Concepts.Chapter import Chapter
from fiction_dl.Concepts.Extractor import Extractor
from fiction_dl.Utilities.Terminal import ReadString

# Standard packages.

from getpass import getpass
import logging
import re
from typing import List, Optional

# Non-standard packages.

from bs4 import BeautifulSoup
from dreamy_utilities.Text import GetDateFromTimestamp, Stringify
from dreamy_utilities.Web import DownloadSoup, GetSiteURL

#
#
#
# The class definition.
#
#
#

class ExtractorXenForo(Extractor):

    def __init__(self, forumURL: str) -> None:

        ##
        #
        # The constructor.
        #
        ##

        super().__init__()

        self._baseURL = GetSiteURL(forumURL)
        self._forumURL = forumURL

    def SupportsAuthentication(self) -> bool:

        ##
        #
        # Checks whether the extractor supports user authentication.
        #
        # @return **True** if the site *does* support authentication, **False** otherwise.
        #
        ##

        return True

    def Authenticate(self) -> bool:

        ##
        #
        # Logs the user in, interactively.
        #
        # @param username The username.
        # @param password The password.
        #
        # @return **True** if the user has been authenticated correctly, **False** otherwise.
        #
        ##

        username = ReadString("Your username")
        if not username:
            return True

        password = getpass(prompt = "Your password: ")

        data = {
            "login": username,
            "password": password,
            "register": 0,
            "remember": "1",
            "cookie_check": "1",
            "_xfToken": "",
        }

        self._session.post(
            url = self._forumURL + "login/login",
            data = data
        )

        return True

    def ExtractChapter(self, index: int) -> Optional[Chapter]:

        ##
        #
        # Extracts specific chapter.
        #
        # @param index The index of the chapter to be extracted.
        #
        # @return **True** if the chapter is extracted correctly, **False** otherwise.
        #
        ##

        if index > len(self._chapterURLs):
            logging.error(
                f"Trying to extract chapter {index}. "
                f"Only {len(self._chapterURLs)} chapter(s) located. "
                f"The story supposedly has {self.Story.Metadata.ChapterCount} chapter(s)."
            )
            return None

        chapterURL = self._chapterURLs[index - 1]

        soup = DownloadSoup(chapterURL, self._session)
        if not soup:
            logging.error(f'Failed to download page: "{chapterURL}".')
            return None

        if -1 != (postIDLocation := chapterURL.find("#")):

            postID = chapterURL[postIDLocation + 1:]

            postElement = soup.find("article", {"data-content": postID}) or soup.select_one(f"#{postID}")
            if not postElement:
                logging.error("Post element not found.")
                return None

            bodyElement = postElement.select_one("div.bbWrapper") or postElement.select_one("div.messageContent")
            if not bodyElement:
                logging.error("Message body element not found.")
                return None

        else:

            postElement = soup.select_one("li.message")
            if not postElement:
                logging.error("Post element not found.")
                return None

            bodyElement = postElement.select_one("div.messageContent")
            if not bodyElement:
                logging.error("Message body element not found.")
                return None

        return Chapter(content = Stringify(bodyElement.encode_contents()))

    def _InternallyScanStory(
        self,
        URL: str,
        soup: Optional[BeautifulSoup]
    ) -> bool:

        ##
        #
        # Scans the story: generates the list of chapter URLs and retrieves the
        # metadata.
        #
        # @param URL  The URL of the story.
        # @param soup The tag soup.
        #
        # @return **False** when the scan fails, **True** when it doesn't fail.
        #
        ##

        # Generate the threadmarks URL.

        threadmarksURL = self._GetThreadmarksURL(self.Story.Metadata.URL)
        if not threadmarksURL:
            logging.error("Failed to generate threadmarks URL.")
            return False

        # Retrieve story metadata.

        soup = DownloadSoup(threadmarksURL, self._session)
        if not soup:
            logging.error(f'Failed to download page: "{threadmarksURL}".')
            return False

        titleElement = soup.select_one("h1.p-title-value") or soup.select_one(".titleBar > h1")
        if not titleElement:
            logging.error("Title element not found.")
            return False

        titleSpanElements = titleElement.find_all("span")
        for element in titleSpanElements:
            element.decompose()

        authorElements = soup.find_all(attrs = {"data-content-author": True})
        if not authorElements:
            logging.error("Author elements not found.")
            return False

        datePublished = int(authorElements[0]["data-content-date"].strip())
        dateUpdated = int(authorElements[-1]["data-content-date"].strip())

        self.Story.Metadata.Title = titleElement.get_text().strip()
        if self.Story.Metadata.Title.endswith("- Threadmarks"):
            self.Story.Metadata.Title = self.Story.Metadata.Title[:-14]
        elif self.Story.Metadata.Title.startswith("Threadmarks for:"):
            self.Story.Metadata.Title = self.Story.Metadata.Title[17:]

        titleProperMatch = re.search("(.+) \(.+\)", self.Story.Metadata.Title)
        if titleProperMatch:
            self.Story.Metadata.Title = titleProperMatch.group(1)

        self.Story.Metadata.Author = authorElements[0]["data-content-author"].strip()
        self.Story.Metadata.Summary = "No summary."

        self.Story.Metadata.DatePublished = GetDateFromTimestamp(datePublished)
        self.Story.Metadata.DateUpdated = GetDateFromTimestamp(dateUpdated)

        self.Story.Metadata.ChapterCount = len(authorElements)
        self.Story.Metadata.WordCount = 0

        # Retrieve chapter URLs.

        chapterLinkElements = soup.select("div.structItem-title a")
        if not chapterLinkElements:
            chapterLinkElements = soup.select(".threadmarkList > ol > li > a")

        for element in chapterLinkElements:

            chapterRelativeURL = element["href"]
            if not chapterRelativeURL.startswith("/"):
                chapterRelativeURL = "/" + chapterRelativeURL

            chapterURL = self._baseURL + chapterRelativeURL

            self._chapterURLs.append(chapterURL)

        if not self._chapterURLs:
            logging.error("Failed to retrieve chapter URLs.")
            return False

        # Return.

        return True

    def _GetThreadmarksURL(self, URL: str) -> Optional[str]:

        ##
        #
        # Retrieves a URL leading to the threadmarks page.
        #
        # @param URL The URL of the story.
        #
        # @return URL leading to the threadmarks page.
        #
        ##

        if not URL:
            return None

        elif URL.endswith("threadmarks"):
            return URL

        threadTitleMatch = re.search("/threads/(.*)/", URL)
        if not threadTitleMatch:
            return None

        threadTitle = threadTitleMatch.group(1)

        return f"{self._forumURL}threads/{threadTitle}/threadmarks"