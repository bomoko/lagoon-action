# Use the uselagoon/lagoon-cli as a base image
FROM uselagoon/lagoon-cli as base

# # Create SSH directory
# RUN mkdir -p ~/.ssh/

# Grab envplate so we can sort out the configuration files
RUN wget -q https://github.com/kreuzwerker/envplate/releases/download/v1.0.2/envplate_1.0.2_$(uname -s)_$(uname -m).tar.gz -O - | tar xz && mv envplate /usr/local/bin/ep && chmod +x /usr/local/bin/ep

# Copy the entry script and set correct permissions
COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

# copy across the lagoon.yaml file
COPY lagoon.yml ~/.lagoon.yml

# Set up environment variable for the SSH key
ENV SSH_PRIVATE_KEY ""
ENV LAGOON_GRAPHQL_ENDPOINT "https://api.lagoon.amazeeio.cloud/graphql"
ENV LAGOON_SSH_HOSTNAME "ssh.lagoon.amazeeio.cloud"
ENV LAGOON_PORT "32222"
ENV LAGOON_COMMAND "whoami"

WORKDIR /

# Entry point to run the custom script
ENTRYPOINT ["/entry.sh"]