# Synthia Bot

Synthia is a feature-rich Discord bot designed to provide real-time updates and enhancements to your server. It specializes in fetching and displaying the latest AI-related news in a dedicated channel, offering an automated news feed experience. Additionally, Synthia is built to demonstrate web scraping skills and runs seamlessly on a Docker container for 24/7 availability.

---
![Synthia](https://i.imgur.com/Pp7Lqi1.jpg)
<!-- ![Synthia](https://i.imgur.com/dtvmhLK.jpg)
![Synthia](https://i.imgur.com/1C3LD34.jpg) -->


## Features

- **Welcome with a Joke:**
   Welcomes new members to your server with a personalized joke, setting a friendly tone for interactions. (Feature under development, nearly complete.)

- **AI News Feed**:
  Automatically fetches the latest AI-related news from top sources and posts it in a specified Discord channel.

- **Web Scraping Integration**:
  Utilizes web scraping techniques to collect fresh and relevant news, serving as a practical example of Python-based scraping.

- **Customizable**:
  Easily configure the channel for news updates and set the frequency of news posts.

- **Dockerized Deployment**:
  Fully containerized with Docker, ensuring portability and ease of deployment.

---

## Installation

### Prerequisites
- Python 3.8+
- Docker (optional, for containerized deployment)
- A Discord bot token (get one from the [Discord Developer Portal](https://discord.com/developers/applications))

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rakinplaban/Discord_chat_miku
   cd Discord_chat_miku
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Create a `.env` file in the root directory.
   - Add your Discord bot token:
     ```env
     BOT_TOKEN=your_discord_bot_token
     ```

4. Run the bot:
   ```bash
   python main.py
   ```

---

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t synthia-bot .
   ```

2. Run the container:
   ```bash
   docker run -d --name synthia-container synthia-bot
   ```

3. Ensure 24/7 availability by hosting the container on a cloud platform like AWS, Azure, or DigitalOcean.

---

## Usage

- Invite Synthia to your Discord server using your bot's invite link.
- Set up the channel where you want AI news to be posted.
- Synthia will start fetching and posting news based on the configured schedule (default: hourly).

---

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - `discord.py` for bot interactions
  - `beautifulsoup4` and `requests` for web scraping
- **Containerization**: Docker

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- Inspired by the desire to automate AI news feeds and practice web scraping techniques.
- Thanks to the open-source community for providing tools and libraries.

---

Enjoy using Synthia! If you encounter any issues or have feature requests, feel free to open an [issue](https://github.com/rakinplaban/Discord_chat_miku/issues) or contact me.

<h1 align="center">
   <img src="https://i.imgur.com/rm70p64.jpg" height="250" width="250"/>
</h1>
