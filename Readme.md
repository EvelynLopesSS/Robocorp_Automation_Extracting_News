# 📰 News Extractor Robot 🤖

This Robocorp robot automates the process of extracting news articles from a target website based on user-defined search criteria. The extracted data is then organized and saved into an Excel spreadsheet.

## ✨ Features

* **Web Scraping**: Extracts news articles from [aljazeera](https://www.aljazeera.com/) website.
* **Data Extraction**: Retrieves article title, description, publication date, image, and URL.
* **Data Processing**:
   - Counts occurrences of a search phrase in the title and description.
   - Determines if the article mentions any monetary values,  recognizing formats like:
      - $11.1
      - $111,111.11
      - 11 dollars
      - 11 USD
      - 11 dollar
   - Downloads and saves news images into a folder named 'Img'.
* **Excel Export**: Organizes extracted data and exports it to an Excel file.
* **Parameterization**:
   - Accepts search phrase, news category, and number of months as input parameters.
   - These parameters are designed to be passed via a Robocloud work item.

## ⚙️ Executing with Robocorp Control Room

1. **Create a Robocorp Control Room Process:**
   * In your Robocorp Control Room, create a new process using the GitHub app integration.
   * Link the process to your repository.
2. **Configure Work Items:**
   * **What is a Work Item?** A work item is like a set of instructions you give your robot each time you want it to run. 
   * Create a work item for the process and provide the following search parameters:
      * **`search_phrase`:** The keyword(s) to search for (e.g., "technology", "artificial intelligence").
      * **`news_category`:**  The category or section of the news website (e.g., "business", "sports").
      * **`number_of_months`:** The number of months back from the current date to retrieve articles.

         **Example**: 
         - "0" or "1": Retrieves articles only from the current month.
         - "2": Retrieves articles from the current and previous month.
         - "3": Retrieves articles from the current month and the two preceding months. 
         - And so on.
3. **Execute the Process:**  Run the process to start the news article extraction. The robot will use the information from your work item to perform the search.

## 📂 Output
The robot generates an 'Img' folder containing downloaded images and an 'Excel' folder with the 'news_data.xlsx' file. To make these accessible as artifacts in Robocorp Control Room, the folders are zipped:
- **Images.zip**: Contains the compressed Img folder.
- **Excel.zip**: Contains the compressed Excel folder.


### 💻 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/EvelynLopesSS/Challange.git
