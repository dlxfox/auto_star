#!/usr/bin/env python3

import csv
import requests
import os
import sys
from typing import Optional, Tuple
import time
from io import StringIO

# Configuration
PAPER_SOURCE_CSV = os.getenv('PAPER_SOURCE_CSV', 'https://raw.githubusercontent.com/dlxfox/read_papers/master/papers.csv')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'get_your_github_token_from https://github.com/settings/tokens/new')
REPO_COLUMN = 'repo_id'

def extract_github_info(repo_id: str) -> Optional[Tuple[str, str]]:
    if not repo_id or repo_id.strip() == '':
        return None
        
    link = repo_id.strip()
    
    # Handle full GitHub URLs
    if link.startswith('https://github.com/'):
        link = link.replace('https://github.com/', '').strip('/')
    elif link.startswith('http://github.com/'):
        link = link.replace('http://github.com/', '').strip('/')
    
    # Split by '/' to get owner and repo
    parts = link.split('/')
    if len(parts) >= 2:
        owner = parts[0]
        repo = parts[1]
        # Remove any additional path components or query parameters
        repo = repo.split('#')[0].split('?')[0]
        return owner, repo
    
    return None

def star_repo(owner: str, repo: str) -> bool:
    url = f'https://api.github.com/user/starred/{owner}/{repo}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json'
    }

    try:
        # Check if already starred
        check = requests.get(url, headers=headers)
        if check.status_code == 204:
            print(f'✅ Already starred: {owner}/{repo}')
            return True
        elif check.status_code == 404:
            # Not starred, so star it
            response = requests.put(url, headers=headers)
            if response.status_code == 204:
                print(f'⭐ Successfully starred: {owner}/{repo}')
                return True
            else:
                print(f'❌ Failed to star: {owner}/{repo}, status code: {response.status_code}')
                return False
        else:
            print(f'⚠️  Check failed: {owner}/{repo}, status code: {check.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'❌ Network error for {owner}/{repo}: {e}')
        return False

def main():
    """Main function to process the CSV file and star repositories"""    
    if GITHUB_TOKEN == 'add_your_github_token':
        print("❌ Error: Please set your GitHub token!")
        print("   Set the GITHUB_TOKEN environment variable or update the script.")
        sys.exit(1)
    
    print(f"🚀 Starting to process {PAPER_SOURCE_CSV}...")
    print(f"📊 Looking for repositories in the '{REPO_COLUMN}' column")
    print("-" * 50)
    
    successful_stars = 0
    failed_stars = 0
    skipped_entries = 0
    
    try:
        with requests.get(PAPER_SOURCE_CSV) as response:
            csv_content = response.text
            csvfile = StringIO(csv_content)
            reader = csv.DictReader(csvfile)
            
            # Verify the required column exists
            if REPO_COLUMN not in reader.fieldnames:
                print(f"❌ Error: Column '{REPO_COLUMN}' not found in CSV!")
                print(f"   Available columns: {', '.join(reader.fieldnames)}")
                sys.exit(1)
            
            for row_num, row in enumerate(reader, start=2):  # Start from 2 to account for header
                repo_id = row.get(REPO_COLUMN, '').strip()
                
                if not repo_id:
                    print(f"⏭️  Skipping row {row_num}: No code link provided")
                    skipped_entries += 1
                    continue
                
                # Extract GitHub info
                github_info = extract_github_info(repo_id)
                if not github_info:
                    print(f"⚠️  Skipping row {row_num}: Invalid GitHub link - {repo_id}")
                    skipped_entries += 1
                    continue
                
                owner, repo = github_info
                
                # Star the repository
                if star_repo(owner, repo):
                    successful_stars += 1
                else:
                    failed_stars += 1
                time.sleep(0.1)

    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        sys.exit(1)
    
    # Summary
    print("-" * 50)
    print("📈 Summary:")
    print(f"   ✅ Successfully starred: {successful_stars}")
    print(f"   ❌ Failed to star: {failed_stars}")
    print(f"   ⏭️  Skipped entries: {skipped_entries}")
    print(f"   📊 Total processed: {successful_stars + failed_stars + skipped_entries}")

if __name__ == '__main__':
    main()