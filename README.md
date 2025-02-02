# crawlmd


## Quicksart


**Crawl a website**
```bash
python main.py https://www.grandlyon.com/
# or
python main.py https://www.grandlyon.com/ --limit 10
```

**Clean the data**
```bash
python main.py --clean www.grandlyon.com
```



## Reflexions

### Cleaning Data


#### Data fetching

#### Data format

- [ ] Remove repeated spaces and punctuation
- [ ] Remove special characters (keep the accents)

**LLM interpretation**

- [ ] Is the article useful? based on context
- [ ] Create an article summary on side for testing
- [ ] Create a list of tags
- [ ] If no description, create one based on the content
- [ ] If not date check is a date is mentionned in the content and use it

#### Article Structure

```markdown
# Title

## Tags

## Description

## Author

## Date

## Content


```