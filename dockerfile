FROM tensorflow/tensorflow:2.8.0
MAINTAINER manguuu <mingyuu.dev@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ Asia/Seoul
ENV PYTHONIOENCODING UTF-8
ENV LC_CTYPE C.UTF-8

WORKDIR /root

RUN apt update
RUN apt install python git curl wget vim zsh python3 python3-pip net-tools nginx sudo -y
RUN python3 -m pip install --upgrade pip

RUN pip install lime
RUN pip install aiofiles
RUN pip install "fastapi[all]"

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
RUN echo "source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc

RUN git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
RUN echo "source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc
RUN echo "ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=111'" >> ~/.zshrc

RUN echo "syntax on\\nfiletype indent plugin on\\nlet python_version_2=1\\nlet python_highlight_all=1\\nset tabstop=8\\nset softtabstop=4\\nset autoindent\nset nu">>~/.vimrc

RUN sudo chsh -s $(which zsh)

RUN git clone https://github.com/manguuu/whatisbreed-backend
RUN git clone https://github.com/manguuu/whatisbreed-frontend

RUN curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
RUN apt install nodejs

EXPOSE 80
EXPOSE 443