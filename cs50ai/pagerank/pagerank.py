import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r'<a\s+(?:[^>]*?)href="([^"]*)"', contents)
            pages[filename] = set(links) - {filename}


    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    distribution = {}
    links = corpus[page]

    if links:

        for linked_page in links:
            distribution[linked_page] = damping_factor / len(links)
        for p in corpus:
            if p in distribution:
                distribution[p] += (1 - damping_factor) / N
            else:
                distribution[p] = (1 - damping_factor) / N
    else:

        for p in corpus:
            distribution[p] = 1 / N

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    sample = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_rank[sample] += 1
        next_distribution = transition_model(corpus, sample, damping_factor)
        sample = random.choices(
            population=list(next_distribution.keys()),
            weights=list(next_distribution.values()),
            k=1
        )[0]
    page_rank = {page: rank / n for page, rank in page_rank.items()}

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = {page: 1 / N for page in corpus}

    while True:
        new_page_rank = {}
        for page in corpus:
            new_rank = (1 - damping_factor) / N
            for potential_linker in corpus:
                if page in corpus[potential_linker]:
                    new_rank += damping_factor * page_rank[potential_linker] / len(corpus[potential_linker])
                if len(corpus[potential_linker]) == 0:
                    new_rank += damping_factor * page_rank[potential_linker] / N
            new_page_rank[page] = new_rank

        if all(abs(new_page_rank[page] - page_rank[page]) < 0.001 for page in page_rank):
            break

        page_rank = new_page_rank

    total = sum(page_rank.values())
    page_rank = {page: rank / total for page, rank in page_rank.items()}

    return page_rank


if __name__ == "__main__":
    main()
