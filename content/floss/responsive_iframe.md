Title: "Responsive" iframes, e.g. for DokuWiki and Shiny
Date: 2016-09-29
Tags: floss, javascript, html, iframe, dokuwiki, shiny
Slug: responsive-iframe
Summary: How to embed a "responsive" (i.e. vertically resizing) iframe in a web page.

Sometimes, the best way to embed an interactive element into a website is to use
an iframe. Obviously, not when your website is a webapp and that element
represents the main functionality it's supposed to provide -- that would be
gross. But when your website is mostly textual / graphical content, typically
authored within a wiki or blogging platform, and you just want to include this
one element to liven it up, iframes are actually a decent (and perhaps the
only?) solution.

Trouble is, you probably want this Frankenstein monster to actually look good,
i.e. seamless if at all possible. But iframes don't have automatic vertical
resizing according to their content, which means you'll need to take care of
that manually. How? By using the JavaScript messaging API for communication
between parent and child frames to send information about window resize events
(from parent to child) and height updates (from child to parent).

Let's imagine you have a [DokuWiki](https://www.dokuwiki.org/dokuwiki#) article
in which you want to embed a small [Shiny](http://shiny.rstudio.com/) app. If
you just embed it in your dokuwiki code using an iframe, taking care to remove
the border and stretch it horizontally...

```html
<html>
<iframe id="embedded-app" src="https://your.shiny.app/url" frameborder="0" width="100%"></iframe>
</html>
```

... this will happen:

![non-responsive iframe](images/non_responsive.png)

Eww, scrollbar. Messaging to the rescue! First of all, you need to teach your
embedded web page to send information about its height to the parent at
appropriate times. This can be achieved by adding this piece of JavaScript to
it:

```javascript
(function() {
  ////////////////////////////////////////////
  // CONFIGURE THESE TO MATCH YOUR USE CASE //
  ////////////////////////////////////////////
 
  // set this to a selector for the element that contains the entire UI
  // you want to access via the iframe -- for a Shiny app, it might be
  // a div with Bootstrap's container-fluid class
  var containerSelector = ".container-fluid";
  
  // this should be the root URL of the parent frame (DokuWiki) which you want
  // to allow to send messages to the child
  var allowedOrigin = "https://dokuwiki.example.com"

  ///////////////////////
  // END CONFIGURATION //
  ///////////////////////

  function sendHeightOf(querySelector) {
    var container = document.querySelector(querySelector);
    if (container.scrollHeight !== undefined) {
      var h = container.scrollHeight;
      parent.postMessage(h, "*");
    } else {
      console.log("No element corresponding to querySelector " + querySelector +
                  " found, or element did not have property scrollHeight.");
    }
  }

  // cross-browser compatible infrastructure
  var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
  var eventer = window[eventMethod];
  var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

  // listen for resize message from parent window (see point ② below)
  eventer(messageEvent, function(e) {
    if (e.origin == allowedOrigin) {
      sendHeightOf(containerSelector);
    } else {
      console.log("Was expecting a message from " + allowedOrigin + ", got "
                  + e.origin + " instead.");
    }
  });

  window.onload = function() {
    // inform parent at least once after load (see point ① below)
    sendHeightOf(containerSelector);

    // monitor self-initiated changes in size (see point ③ below)
    var mo = new MutationObserver(function() {
      sendHeightOf(containerSelector);
    });
    mo.observe(document, {subtree: true, childList: true, characterData: true});
  };
})();
```

What are these "appropriate times" mentioned above? The code above implements
the following ones, which should be generic enough to cover most situations:

1. on initial page load
2. on window resize (see below, the parent frame has to send a message to the
   child frame that it has been resized, to which the child responds with a size
   update message)
3. on any kind of mutation of the DOM inside the child frame (not a full reload
   of the entire page, that would be handled by point ① above), which might
   affect the size of the rendered component

On the parent (DokuWiki) side, you then need to handle the incoming size update
messages from the child frame, and sending resize messages when the window is
resized. This can be achieved with the following DokuWiki markup:

```html
<html>
<iframe id="embedded-app" src="https://your.shiny.app/url" frameborder="0" width="100%"></iframe>
<script>
(function() {
  ////////////////////////////////////////////
  // CONFIGURE THESE TO MATCH YOUR USE CASE //
  ////////////////////////////////////////////

  // this should be the root URL of the child frame (Shiny app) which you want
  // to allow to send messages to the parent
  var allowedOrigin = "https://your.shiny.app"

  ///////////////////////
  // END CONFIGURATION //
  ///////////////////////

  var embeddedApp = document.getElementById("embedded-app");

  function resizeIframe(pixels) {
      embeddedApp.style.height = pixels + "px";
  }

  // cross-browser compatible infrastructure
  var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
  var eventer = window[eventMethod];
  var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

  // listen to message from iframe
  eventer(messageEvent, function(e) {
    if (e.origin === allowedOrigin) {
      var key = e.message ? "message" : "data";
      var data = e[key];
      resizeIframe(data);
    } else {
      console.log("Was expecting a message from " + allowedOrigin + ", got " + e.origin + " instead.");
    }
  }, false);

  // send message to iframe on window resize
  window.onresize = function() {
    embeddedApp.contentWindow.postMessage("parentWindowResized", "*");
  };
})();
</script>
</html>
```

And the result?

![responsive iframe](images/responsive.png)

Yay! And of course, the iframe gets resized as needed when display conditions
change:

![responsive iframe rearranged](images/responsive_rearranged.png)

Cue bittersweet feeling after having figured out a workaround for such a
specific use case that you're [not quite sure](https://xkcd.com/1205/) it was
worth putting all that effort into it in the first place...
