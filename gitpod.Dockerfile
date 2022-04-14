# This will pull the official Gitpod `vnc` image
# which has much of what you need to start
FROM gitpod/workspace-full-vnc

USER gitpod

# Install tkinter
RUN sudo apt-get update && \
    sudo install-packages tk-dev
