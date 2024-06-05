FROM nginx:alpine-slim
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy in static pages for CSS etc.
COPY ./nginx/static/ /etc/nginx/html/static/

# Copy in static pages from subprojects (Sphinx, Mkdocs, etc.)
COPY ./digital-hospitals-docs/build/html /etc/nginx/html/dev/specs