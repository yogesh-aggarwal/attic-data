all:
	@make queries
	@make urls
	@make products

queries:
	@poetry run generate_queries

urls:
	@poetry run scrape_urls

products:
	@poetry run scrape_products

