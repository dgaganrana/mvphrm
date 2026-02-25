#!/bin/bash
# Orchestrate MVPHRM services with Docker Compose

set -e

COMMAND=$1
SERVICE=$2

show_help() {
  echo "Usage: ./run.sh {start|stop|restart|rebuild [service]|logs|status|help}"
  echo
  echo "Commands:"
  echo "  start             Start all services in detached mode (build only if needed)"
  echo "  stop              Stop all services and remove containers/networks (volumes persist)"
  echo "  restart           Stop then start all services"
  echo "  rebuild [service] Rebuild all services (or a specific service) without using cache"
  echo "  logs              Show and follow logs for all services"
  echo "  status            Show running containers and their status"
  echo "  help              Show this help message"
}

case "$COMMAND" in
  start)
    echo "Starting MVPHRM services..."
    docker-compose up -d
    ;;
  stop)
    echo "Stopping MVPHRM services..."
    docker-compose down
    ;;
  restart)
    echo "Restarting MVPHRM services..."
    docker-compose down
    docker-compose up -d
    ;;
  rebuild)
    if [ -z "$SERVICE" ]; then
      echo "Rebuilding all services..."
      docker-compose build --no-cache
    else
      echo "Rebuilding service: $SERVICE"
      # docker-compose build --no-cache $SERVICE
      docker-compose build $SERVICE
    fi
    ;;
  logs)
    echo "Showing logs for all services..."
    docker-compose logs -f
    ;;
  status)
    echo "Showing container status..."
    docker-compose ps
    ;;
  help)
    show_help
    ;;
  *)
    show_help
    exit 1
    ;;
esac
