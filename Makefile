all:
	@make metadata
	@make queries
	@make urls
	@make products


metadata:
	@poetry run generate_metadata

queries:
	@poetry run generate_queries

urls:
	@poetry run scrape_urls

products:
	@poetry run scrape_products
