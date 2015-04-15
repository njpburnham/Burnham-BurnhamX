var sidebarForThread = new WeakMap(); //A Map is an arbitrary value for the value
var sidebarTemplatePromise = null;

InboxSDK.load('1', 'BurnhamX').then(function(sdk) {


    // the SDK has been loaded, now do something with it!
    sdk.Compose.registerComposeViewHandler(function(composeView) {

        // a compose view has come into existence, do something with it!
        composeView.addButton({
            title: "Burnham w/InboxSDK",
            iconUrl: 'images/BEye.png',
            onClick: function(event) {
                event.composeView.insertTextIntoBodyAtCursor('Hello Burnham!');
            },
        });
    });

    // LIST VIEW
    sdk.Lists.registerThreadRowViewHandler(function(threadRowView) {
        var curr_id = threadRowView.getThreadID();
        // We need to replace this with an API calls
        var url = "https://burnham-x.appspot.com/association/?thread_id=" + curr_id;
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) {
                if (data.count >= 1) {
                    addImageToThread(threadRowView)
                }
            }
        });
    });


    sdk.Conversations.registerMessageViewHandler(function(messageView) {
        var threadView = messageView.getThreadView();

        var url = "https://burnham-x.appspot.com/association/?thread_id=" + threadView.getThreadID();
        $.ajax({
            url: url,
            type: "GET",
            success: function(data) { //
                if (data.count >= 1) {
                    $.ajax({
                        url: "https://burnham-x.appspot.com/opportunity/" + data.results[0].opportunity + "/",
                        type: "GET",
                        success: function(oppData) {
                            addBurnhamSideBar(threadView, oppData);
                        }
                    });
                }
            }
        });


    });
});


function addImageToThread(threadRowView) {
    threadRowView.addImage({
        imageUrl: chrome.runtime.getURL("images/BEye.png"),
        tooltip: "Associated",
    });
}

function addBurnhamSideBar(threadView, oppData) {
    if (!sidebarForThread.has(threadView)) {
        sidebarForThread.set(threadView, document.createElement('div'));

        threadView.addSidebarContentPanel({
            el: sidebarForThread.get(threadView),
            title: "BurnhamX",
            iconUrl: chrome.runtime.getURL('images/BEye.png')
        });
    }


    var source = '<div class="column"><h4>Association Found</h4>Customer: Cloudbakers <br />Address: 641 W Lake Street <br /><h3>{{name}}</h3></div>';
    var template = Handlebars.compile(source);
    var context = {
        name: oppData.name,
        

    };
    var html = template(context);
    sidebarForThread.get(threadView).innerHTML = sidebarForThread.get(threadView).innerHTML + html;
}

function get(url, params, headers) {
    $.ajax({
        url: url,
        type: "GET",
        data: params,
        headers: headers,
        success: function(data) {
            console.log(data.results[0].thread_id)
            return data.results;
        }
    });
}