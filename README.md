# sentiment

_sentiment_ is showcasing [_lymph_](https://github.com/deliveryhero/lymph),
a framework for Python services. It's built by Delivery Hero.
It's answering the industries' hottest question:

> How do people feel about pizza?

## Introduction
Let's say you want to know how people feel about "pizza" at this very moment?
It's important for you, because maybe you're running a food ordering platform.
Your marketing department wants to know what customers want or monitor the
impact of a campaign.

Simply asking people won't work. People don't like to answer questionnaires,
nor do they like to participate in surveys. There's one thing people like to do
a lot, however. People love to tweet. That's basically an invitation. Let's tap
the wire. That is, let's tap the _twittersphere_.

So, we'll build a tool for monitoring people's "sentiment" towards pizza.
We're going to build it with services.  The data source will be twitter, we'll
analyze tweets, store them and display results via a minimal website. We will
build the following services to achieve that goal.

### Inbound

This service is listening to tweets. It utilises Twitter's Streaming API. You
can filter for tweets with certain keywords and get them via a stream. This
service filters for the term "pizza". Every time such a tweet is received an
event `item.received` is emitted with the content attached as its body.

To configure this service create an application on Twitter
[here](https://apps.twitter.com/) and add its credentials to
`inbound/inbound.yml`.

### Crunching

The responsibility of `crunching` is the ingestion of the tweets captured by
`inbound`. However, this service does not know anything about `inbound` itself.
It only subscribes to the `item.received` event, computes its _polarity_
and indexes the tweet in Elasticsearch.

For the computation of the polarity of a tweet we're using [TextBlob](http://textblob.readthedocs.org).
It computes a text's [polarity](http://textblob.readthedocs.org/en/dev/api_reference.html?highlight=subjectivity#textblob.blob.BaseBlob.polarity)
in an interval of 1 and -1.

Furthermore, we're exposing two RPC methods, `avg`(returns avg polarity) and
`count`(returns number of ingested tweets).

Technically, having both the ingestion and RPC methods on one interface isn't
sound. That means these two cannot be scaled individually.  However, we'll
stick with it to keep things simple.

### Barometer

Finally, there's `barometer` displaying the average polarity of collected tweets
as a webpage. It's overly simple. It has one endpoint and returns html in its
response. The page's body colour is representing the average polarity going from
red (-1) to green (1). It also shows the average and the count as numbers.

### Overview
![The services](https://www.evernote.com/shard/s245/sh/fe91bde3-1b70-4088-a287-2edd4d2b15fd/d5d833d62785cf1b44caa8160b95ce02/res/2ad86331-4d25-4ed5-9e92-dc8512c9e767/skitch.png)

## Setup
We'll use [fig](https://fig.sh) and docker to run our services. Make sure you
have all relevant docker tools installed. Getting `fig` is as simple as:
``` shell
$ pip install fig
```
Firstly, we need to build the containers:
``` shell
$ fig build
```
This will take a while as it's pulling the images and installing dependencies.
Next, we bring up the cluster:
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

When peeking into logs with `fig logs crunching` you should see that all
instances are targeted by requests.

Sclaing down works via:
``` shell
$ fig scale crunching=1
```

## Serving worldwide
To make things more fun we'll make _sentiment_ accessible over the internet
with [ngrok](https://ngrok.com):

``` ngrok
ngrok <docker_ip>:4080
```

Enjoy!
