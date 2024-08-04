Idea: save and load items to the mongodb

Bonus: pydantic? 

a) Pick a database:
   ⭐️ MongoDB
   - Postgre
   - Some vector storage like qdrant?
   - Logging - redis, elk? Dashboard? 
   - Bonus: LLM logging

b) Launch database instances and copy credentials:
   - [ ] Local
   - [ ] Coolify
   - Bonus: cloud (launched already)
     - Copy creds
     - Cleanup schlack
   - Bonus: web UI for mongo

c) Test UI access and save credentials:
   - [ ] Cloud
   - [ ] Local
   - [ ] Coolify

d) Write docs and usage examples:
   - [ ] Type annotations and docstrings
   - [ ] Examples GitHub repo:
   - [ ] Basic usage, json
   - [ ] Telegram message history
   - [ ] Aiogram user data and ...
   - [ ] Aioscheduler
   - Bonus: gpt scenarios, conversation chains
   - Bonus: notes, todos, knowledge etc.

## Bonus
- Design lib interface:
  - Client.get_db()
  - -> get collection (gets obj)
  - -> load collection (gets all items)
- Data ingestion (Drag&drop folder somewhere -> log in console)

## Suggestions from Claude
- Create Python wrapper:
  - Connection setup
  - CRUD operations
  - Text indexing and search
- More features
   - Caching
   - Pagination
   - Bulk operations

