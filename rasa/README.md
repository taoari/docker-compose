# Rasa Hello

### Training the Model

To train your Rasa model, use the following command:

```bash
rasa train
```

### Running the Rasa Server

You need to open two terminal windows to run the Rasa server and actions server:

**Terminal 1:**

```bash
rasa run --enable-api --cors "*" --debug
```

**Terminal 2:**

```bash
rasa run actions --debug
```

### Testing the Setup

You can test your setup using either the terminal or by accessing the `webui/index.html` file.

**Using Terminal:**

```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook -d '{"sender": "default", "message": "Hi"}'
```

## Docker Demo Setup

**Train the Model (One-Time Setup):**

```bash
docker compose build

docker run -v .:/app rasa/rasa:3.6.20-full train
# Alternatively:
docker run -v .:/app rasa-hello train
```

**Set Up the Demo:**

```bash
docker compose up -d
docker compose down
```

You can access the demo at [http://localhost:5000/](http://localhost:5000/).

## Learning Resources

### Rasa Fallback

[Learn about Rasa Fallback](https://rasa.com/docs/rasa/fallback-handoff/)

### Custom Actions

[Explore Custom Actions](https://github.com/RasaHQ/conversational-ai-course-3.x)


### Custom Graph Components

[Explore Custom Graph Components](https://rasa.com/docs/rasa/custom-graph-components/)