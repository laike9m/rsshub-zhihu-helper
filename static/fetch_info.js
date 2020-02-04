var rsshubAddr = null;

$.get(`http://localhost:8000/api/rsshub_addr`, addr => {
  rsshubAddr = addr;
  console.log(`rsshubAddr set to ${rsshubAddr}`);
});

$("#search-button").click(() => {
  const searchTerm = $("#search-box").val() || "轮子哥";
  $("#candiate_list").empty();
  $.get(`http://localhost:8000/api/search_user/${searchTerm}`, data => {
    data.forEach((userInfo) => {
      renderUser(userInfo['name'], userInfo['url_token'], userInfo['avatar_url'])
    })
  });
});

function renderUser(name, urlToken, avatarUrl) {
  console.assert(rsshubAddr, "rsshubAddr is null. Check your local server status.");
  const feedUrl = `${rsshubAddr}/zhihu/people/activities/${urlToken}`;
  $("#candiate_list")
    .append(
      $(`<p><img src=${avatarUrl} />&nbsp;${name}</p>`)
      .append(
        $("<button class='pick'>Pick</button>").click(() => {
          $("#chosen_user").append(
            $(`<p><img src=${avatarUrl} />&nbsp;&nbsp;${name}</p>`)
            .attr("data-feed", feedUrl));
        })
      )
      .append(
        $("<button class='remove'>Remove</button>").click(() => {
          $(`p[data-feed="${feedUrl}"`).remove()
        })
      )
    );
}

$("#dump-opml").click(() => {
  let feeds = [];
  $("#chosen_user p").each((_, elem) => {
    feeds.push($(elem).attr('data-feed'));
  });
  $.post({
    url: "http://localhost:8000/api/dump",
    data: JSON.stringify({
      'feeds': feeds
    }),
    dataType: 'json',
    success: resp => {
      alert(resp);
    }
  });
});