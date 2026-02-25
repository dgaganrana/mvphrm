FROM postgres:15-alpine

# Keep image generic — no secrets here
COPY init.sql /docker-entrypoint-initdb.d/
