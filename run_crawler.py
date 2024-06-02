from tasks import run_crawler

if __name__ == "__main__":
    result = run_crawler.delay(
        "https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list"
    )
    print(f"Task ID: {result.id}")
