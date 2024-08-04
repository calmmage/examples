Understood. I'll guide you through the local setup first:

**Local Setup**
1. Open Docker on your machine
2. In terminal, run:
   ```
   docker pull mongo
   ```
3. Launch container:
   ```
   docker run -d -p 27017:27017 --name mongodb mongo
   ```
4. Test access:
   ```
   docker exec -it mongodb mongosh
   ```

Shall I continue with Coolify setup next?
