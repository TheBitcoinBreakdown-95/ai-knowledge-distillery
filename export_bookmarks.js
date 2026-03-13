// X/Twitter Bookmarks Exporter (GraphQL Interception)
// Usage: Navigate to x.com/i/bookmarks, open DevTools Console, paste this script, press Enter.
// The script intercepts Twitter's internal GraphQL API to capture raw tweet data,
// auto-scrolls through all bookmarks, then downloads bookmarked_tweets.json.
//
// Approach: Monkey-patches window.fetch to intercept /graphql/ responses.
// This is more reliable than DOM scraping -- gets raw structured data, resilient to UI changes.
// Inspired by Siftly (github.com/viperrcrypto/Siftly).

(function () {
  const bookmarks = [];
  const seenIds = new Set();
  const SCROLL_INTERVAL = 1000;
  const SCROLL_STEP = 5000;
  let previousCount = 0;
  let unchangedCount = 0;
  const MAX_UNCHANGED = 8;

  function extractTweetData(tweetResult) {
    try {
      const tweet = tweetResult.tweet || tweetResult;
      const legacy = tweet.legacy;
      if (!legacy) return null;

      const id = tweet.rest_id || legacy.id_str;
      if (!id || seenIds.has(id)) return null;

      const userResult = tweet.core?.user_results?.result;
      const userLegacy = userResult?.legacy;

      const handle = userLegacy?.screen_name || '';
      const displayName = userLegacy?.name || '';

      // Full text
      const text = legacy.full_text || legacy.text || '';

      // Timestamp
      const datetime = legacy.created_at || '';

      // Media
      const media = [];
      const extMedia = legacy.extended_entities?.media || legacy.entities?.media || [];
      for (const m of extMedia) {
        if (m.type === 'photo') {
          media.push({ type: 'photo', url: m.media_url_https });
        } else if (m.type === 'video' || m.type === 'animated_gif') {
          const variants = m.video_info?.variants || [];
          const mp4s = variants.filter(v => v.content_type === 'video/mp4');
          const best = mp4s.sort((a, b) => (b.bitrate || 0) - (a.bitrate || 0))[0];
          media.push({
            type: m.type === 'animated_gif' ? 'gif' : 'video',
            url: best ? best.url : (m.media_url_https || '')
          });
        }
      }

      // URLs (expanded, not t.co)
      const urls = (legacy.entities?.urls || []).map(u => u.expanded_url).filter(Boolean);

      // Hashtags
      const hashtags = (legacy.entities?.hashtags || []).map(h => h.text);

      // Engagement
      const likes = legacy.favorite_count || 0;
      const retweets = legacy.retweet_count || 0;
      const replies = legacy.reply_count || 0;
      const views = tweet.views?.count || '0';

      // Is this an article / long-form?
      const isArticle = text.length > 500 ||
        urls.some(u => u.includes('/i/article/')) ||
        (legacy.entities?.urls || []).some(u => (u.title || '').length > 50);

      seenIds.add(id);
      return {
        id,
        url: `https://x.com/${handle}/status/${id}`,
        handle,
        displayName,
        text,
        datetime,
        media,
        urls,
        hashtags,
        likes,
        retweets,
        replies,
        views,
        isArticle
      };
    } catch (e) {
      return null;
    }
  }

  function processGraphQLResponse(data) {
    try {
      // Walk the response to find tweet entries (nested in instructions -> entries)
      const instructions = data?.data?.bookmark_timeline_v2?.timeline?.instructions ||
                           data?.data?.bookmark_timeline?.timeline?.instructions ||
                           [];

      for (const instruction of instructions) {
        const entries = instruction.entries || [];
        for (const entry of entries) {
          const tweetResult = entry.content?.itemContent?.tweet_results?.result;
          if (tweetResult) {
            // Handle tweets that are wrapped in a "tweet" property (tombstones, etc)
            const actual = tweetResult.__typename === 'TweetWithVisibilityResults'
              ? tweetResult.tweet
              : tweetResult;

            if (actual && actual.__typename === 'Tweet') {
              const extracted = extractTweetData(actual);
              if (extracted) {
                bookmarks.push(extracted);
                console.log(`[${bookmarks.length}] @${extracted.handle}: ${extracted.text.slice(0, 60)}...`);
              }
            }
          }
        }
      }
    } catch (e) {
      // Silently skip non-bookmark responses
    }
  }

  // Intercept fetch to capture GraphQL responses
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const response = await origFetch.apply(this, args);
    try {
      const url = args[0] instanceof Request ? args[0].url : String(args[0]);
      if (url.includes('/graphql/') && url.includes('Bookmark')) {
        const clone = response.clone();
        const data = await clone.json();
        processGraphQLResponse(data);
      }
    } catch (e) {
      // Don't break Twitter if parsing fails
    }
    return response;
  };

  // Also intercept XMLHttpRequest for older code paths
  const origXHRSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (...args) {
    this.addEventListener('load', function () {
      try {
        if (this.responseURL && this.responseURL.includes('/graphql/') && this.responseURL.includes('Bookmark')) {
          const data = JSON.parse(this.responseText);
          processGraphQLResponse(data);
        }
      } catch (e) {}
    });
    return origXHRSend.apply(this, args);
  };

  // Auto-scroll
  const scrollTimer = setInterval(() => {
    window.scrollBy(0, SCROLL_STEP);

    if (bookmarks.length === previousCount) {
      unchangedCount++;
      console.log(`No new bookmarks (${unchangedCount}/${MAX_UNCHANGED}). Total: ${bookmarks.length}`);
      if (unchangedCount >= MAX_UNCHANGED) {
        clearInterval(scrollTimer);
        // Restore original fetch/XHR
        window.fetch = origFetch;
        XMLHttpRequest.prototype.send = origXHRSend;
        console.log(`Done! Captured ${bookmarks.length} bookmarks. Downloading...`);
        download();
      }
    } else {
      unchangedCount = 0;
    }
    previousCount = bookmarks.length;
  }, SCROLL_INTERVAL);

  function download() {
    const output = { bookmarks, exportedAt: new Date().toISOString(), count: bookmarks.length };
    const blob = new Blob([JSON.stringify(output, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'bookmarked_tweets.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
    console.log('Download complete. File: bookmarked_tweets.json');
  }

  console.log('Bookmark exporter started (GraphQL interception). Scroll through bookmarks or wait for auto-scroll...');
  console.log('The script captures data from Twitter API responses as you scroll.');
})();
