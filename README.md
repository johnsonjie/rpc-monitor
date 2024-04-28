# rpc-monitor
### how to use
change config.yaml, monitor the rpc endpoint you need, for example
```
- "node": "rpc-custom"
  "url": "https://192.168.1.2:8545"
```

docker compose build && docker compose up -d

### pull metrics from prometheus
```
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 10s
    static_configs:
      - targets:
        - 'xxxx:8000'  # rpc-monitor-exporter address
```