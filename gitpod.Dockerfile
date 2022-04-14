# This will pull the official Gitpod `vnc` image
# which has much of what you need to start
FROM gitpod/workspace-full-vnc

USER gitpod

# Install tkinter
RUN sudo apt update \
 && sudo apt install -y \
  python-tk  \
 && sudo rm -rf /var/lib/apt/lists/*

