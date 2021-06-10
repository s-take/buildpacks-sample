FROM python:3.7-slim-buster

LABEL io.buildpacks.stack.id="io.github.stake.samples.debian"

RUN addgroup --gid 1000 builder
RUN useradd -ms /bin/bash -u 1000 -g 1000 builder

USER builder

WORKDIR /home/builder

ENV CNB_STACK_ID="io.github.stake.samples.debian"
ENV CNB_USER_ID="1000"
ENV CNB_GROUP_ID="1000"