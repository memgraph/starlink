FROM memgraph/memgraph:2.2.1

USER root

# Install pip packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the local query modules
COPY transformations/ /transformations

USER memgraph
