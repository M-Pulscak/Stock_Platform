from providers.universe.wikipedia_sp500_provider import WikipediaSP500Provider

provider = WikipediaSP500Provider()

members = provider.get_members()

print(len(members))
print(members[:5])