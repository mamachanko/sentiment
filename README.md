# sentiment

_sentiment_ is showcasing [_lymph_](https://github.com/deliveryhero/lymph),
a framework for Python services. It's built by Delivery Hero.
It's answering the industries' hottest question:

> How do people feel about pizza?

## Introduction
Let's say you want to know how people feel about "pizza" at this very moment? It's important for you, because maybe you're running a food ordering platform. Your marketing department wants to know what customers want or monitor the impact of a campaign.

Simply asking people won't work. People don't like to answer questionnaires, nor do they like to participate in surveys. There's one thing people like to do a lot, however. People love to tweet. That's basically an invitation. Let's tap the wire. That is, let's tap the twittersphere.

So, we'll build a tool for monitoring people's "sentiment" towards pizza.
We're going to build it with services.
The data source will be twitter, we'll analyze tweets, store them and
display results via a minimal website. We will build the following services
to achieve that goal.

### Inbound

This service utilises Twitter's Streaming API. You can filter for tweets with certain keywords and get them via a stream. This service filters for the term "pizza". Everytime such a tweet is received an event `item.received` is emitted with the content attached as its body.

### Crunching
wip

### Barometer

![The services](https://www.evernote.com/shard/s245/sh/fe91bde3-1b70-4088-a287-2edd4d2b15fd/d5d833d62785cf1b44caa8160b95ce02/res/2ad86331-4d25-4ed5-9e92-dc8512c9e767/skitch.png)

## Setup
We'll use [fig](https://fig.sh) and docker to run our services. Make sure you have all relevant docker tools installed. Getting `fig` is as simple as:
``` shell
$ pip install fig
```
The containers are built and launched with:
``` shell
$ fig up -d
```
That's it. We've got _sentiment_ running.
Go to `http://<container_ip>:4080` and see for yourself how people feel.


## Scaling

Let's have more instances of `crunching`:
``` shell
$ fig scale crunching=3
```

When peeking into logs with `fig logs crunching` you should see that all instances are targeted by requests.

Sclaing down works via:
``` shell
$ fig scale crunching=1
```

## Serving worldwide
To make things more fun we'll make _sentiment_ accessible over the internet with [ngrok](https://ngrok.com):

``` ngrok
ngrok <docker_ip>:4080
```

Enjoy!
