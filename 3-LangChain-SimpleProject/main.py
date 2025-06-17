from chains.book_chain import book_chain
from chains.tech_chain import tech_chain
from tools.wiki_tool import mock_wikipedia_summary, get_news_summary
from schemas.response_schema import BookRecommendation, TechTrend, CombinedResponse

import json

# Step 1: Get user input
topic = input("Enter a topic (e.g., AI, space, fintech): ")
country = input("Enter a country to explore tech trends: ")

# Step 2: Run chains
# books_raw = book_chain.run({"topic": topic})
# tech_raw = tech_chain.run({"country": country})

books_raw = book_chain.invoke({"topic": topic}).content
tech_raw = tech_chain.invoke({"country": country}).content

# 🔵 Step 3: Call external tool (news API)
news_raw = get_news_summary(topic)

wiki = mock_wikipedia_summary(topic + " in " + country)

# Step 3: Simulate post-processing to structured format
books = [BookRecommendation(title=line.split(". ")[0], summary=line.split(". ")[1])
         for line in books_raw.split("\n") if ". " in line]

techs = [TechTrend(trend=line.split(":")[0], explanation=line.split(":")[1])
         for line in tech_raw.split("\n") if ":" in line]

# Step 4: Validate with Pydantic
response = CombinedResponse(books=books, tech_trends=techs, wiki_summary=news_raw)

# Step 5: Show response
print("\n📚 Smart Assistant Result:\n")
print(json.dumps(response.model_dump(), indent=2))


