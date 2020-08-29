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
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
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
    model = dict()

    # Check if page has no outgoing links
    if len(corpus[page]) == 0:
        # Set probability to be equal among all pages of corpus
        for filename in corpus.keys():
            model[filename] = 1 / len(corpus)
    else:
        # Compute probability to visit each page using formula described above
        for filename in corpus.keys():
            if filename in corpus[page]:
                model[filename] = (damping_factor / len(corpus[page]))
            else:
                model[filename] = 0.0
            model[filename] += (1 - damping_factor) / len(corpus)

    return model
        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    random.seed()

    pagerank = dict()

    # Initialize all PageRank values to 0
    for filename in corpus.keys():
        pagerank[filename] = 0.0

    previous_page = None

    # Iterate through n samples
    for sample in range(n):
        # The first page is chosen at random out of all pages
        if sample == 0:
            previous_page = random.choice(list(corpus.keys()))        
            pagerank[previous_page] = 1.0 / n
        # Otherwise, the next page is based off the previous page transition model
        else:
            prev_sample = transition_model(corpus, previous_page, damping_factor)

            sorted_sample = sorted(prev_sample.items(), key=lambda x: x[1])

            distribution = list()

            # Randomly choose a page based on the transition model
            random_number = random.random()
            
            for i, page in enumerate(sorted_sample):
                if i == 0:
                    distribution.append(page[1])
                else:
                    distribution.append(page[1] + distribution[i-1])

            for i, probability in enumerate(distribution):
                if random_number < probability:
                    previous_page = sorted_sample[i][0]
                    pagerank[previous_page] += 1.0 / n
                    break
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    # Initialize PageRank values to 1 / N where N is number of pages in corpus
    for page in corpus.keys():
        pagerank[page] = 1 / len(corpus)
        # Update corpus if a page has no outgoing links so that the page has links
        # to every page
        if len(corpus[page]) == 0:
            update_dict = dict()
            update_dict[page] = set(
                key for key in corpus.keys() 
            )
            corpus.update(update_dict)

    incoming_links = dict()

    # Get incoming links for each page
    for page in pagerank.keys():
        incoming_links[page] = set(
            key for key, val in corpus.items() if page in val 
        )

    flag = False

    all_converge = set()

    # Continously update PageRank values for each page until
    # each page's PageRank value doesn't change by more than 0.001
    while not flag:
        new_dict = dict()

        for page in pagerank.keys():
            sum = 0
            new_value = 0

            for link in incoming_links[page]:
                if len(corpus[link]) > 0:
                    sum += pagerank[link] / len(corpus[link])

            new_value = (1 - damping_factor) / len(corpus) + (damping_factor * sum)

            if abs(new_value - pagerank[page]) < 0.001 and page not in all_converge:
                all_converge.add(page)

            new_dict[page] = new_value
            
        pagerank.update(new_dict)
 
        if len(all_converge) == len(corpus):
            flag = True

    return pagerank

if __name__ == "__main__":
    main()
