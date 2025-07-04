from langchain_community.document_loaders import WebBaseLoader

def scrape_web_pages(urls):
    """Scrape and return page contents using LangChain's WebBaseLoader."""
    all_contents = []

    for url in urls:
        print(f"\n[+] Scraping: {url}")
        loader = WebBaseLoader(url)
        try:
            docs = loader.load()
            for doc in docs:
                content = doc.page_content.strip()
                print(f"--- {url} ---\n{content[:500]}...\n")  # Preview first 500 chars
                all_contents.append({"url": url, "content": content})
        except Exception as e:
            print(f"[-] Failed to scrape {url}: {e}")

    return all_contents

# Example usage
if __name__ == "__main__":
    urls_to_scrape = [
        "https://medium.com/@karisallan237/anonymous-ftp-pentest-2eeaee790d41"
    ]
    results = scrape_web_pages(urls_to_scrape)
