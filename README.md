# Auto Star Papers in a Single CMD 📚⭐
This tool reads a CSV file containing research papers and automatically stars their associated GitHub repositories on your GitHub account. It's perfect for:

- Academic researchers who want to keep track of interesting papers
- Students building their GitHub star collection
- Anyone who wants to systematically star repositories from a curated list

## 📋 Prerequisites

- Python 3.6 or higher
- A GitHub Personal Access Token

## 🚀 Quick Start

> [!NOTE]
> 1. This script is designed to be run on a local machine without cloning the repository.
> 2. Runing with `python -c "curl -s URL"` is recommended, because it avoids the need to clone the repository and keep your token private :)
> 3. ⚠️ We detach the paper source from this repository, and get the paper source from [dlxfox/read_papers](https://github.com/dlxfox/read_papers) repository, so you can contribute to the paper list by opening a pull request to [dlxfox/read_papers](https://github.com/dlxfox/read_papers).

### 1. Creating a personal access token (classic)
Before running the script, you need to create a personal **access token (classic)** by navigating to [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new). Select scopes `repo` to star public and private repositories.

<img width="891" alt="image" src="https://github.com/user-attachments/assets/5b9a7a89-3e72-4726-b58c-7f4a2fd6c833" />


**⚠️ Important:** Keep your token secure and never commit it to version control!

### 2. Prepare Your CSV File

We manage the CSV file in [dlxfox/read_papers](https://github.com/dlxfox/read_papers/blob/master/papers.csv) to avoid any security access issues in google sheets or tencent docs. At a cost, you must manually fork the [dlxfox/read_papers](https://github.com/dlxfox/read_papers) and update the CSV file when you want to add or remove a paper (it can be done in a few clicks, and you can get feedback from more people):

- fork the [dlxfox/read_papers](https://github.com/dlxfox/read_papers) by clicking the `Fork` button in the top right corner of the page.
- in your forked repository, click the `papers.csv` file and click the `Edit` button, fill in the paper information and click the `Save` button.
- open a pull request to [dlxfox/read_papers](https://github.com/dlxfox/read_papers) to update the CSV file, it can be see by more people.


### 3. Run the Script

```bash
export GITHUB_TOKEN= # your github token from https://github.com/settings/tokens/new
python -c "$(curl -fsSL https://raw.githubusercontent.com/dlxfox/auto_star/master/auto_star.py)"
```

**⚠️ Important:** By default, the script will read the CSV file from [dlxfox/read_papers](https://github.com/dlxfox/read_papers/blob/master/papers.csv). You can also set the `PAPER_SOURCE_CSV` environment variable to your github paper source url if you don't want to open a pull request. In this case, the script will read the CSV file from your `PAPER_SOURCE_CSV` url, which in the format of `https://raw.githubusercontent.com/your_github_username/your_paper_source_repo/master/papers.csv`.

## 📊 CSV File Format

The script expects a CSV file with the following structure. Note that the `repo_id` is recommended to be in the format of `owner/repo-name` to simplify the csv parsing.

| Column | Description | Required |
|--------|-------------|----------|
| `paper_id` | Paper ID | ✅ Yes |
| `repo_id` | GitHub repository link or owner/repo format | ✅ Yes |
| `title` | Paper title | ✅ Yes |
| `summary` | Paper summary | ✅ Yes |

Example CSV Content:
```csv
paper_id,repo_id,title,summary
1,username/repo-name,Example Paper,This is an example paper with code
2,...
```

## 📈 Output

The script provides detailed feedback:

```
🚀 Starting to process papers.csv...
📊 Looking for repositories in the 'repo_id' column
--------------------------------------------------
✅ Already starred: username/repo-name
⭐ Successfully starred: username/repo-name
⚠️  Skipping row 3: Invalid GitHub link - invalid-repo-id
--------------------------------------------------
📈 Summary:
   ✅ Successfully starred: 2
   ❌ Failed to star: 0
   ⏭️  Skipped entries: 1
   📊 Total processed: 3
```

## 📄 License

This project is open source. Please check the license file for details.
---

**Happy Starring! ⭐**
