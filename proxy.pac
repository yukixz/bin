var GOAGENT = 'PROXY 127.0.0.1:8087';
var SSH = 'SOCKS5 127.0.0.1:7070';
var SHADOW = 'SOCKS5 127.0.0.1:7080';

function FindProxyForURL(url, host) {

		proxy = SHADOW;
	if (host == "t.co")		return proxy;
	if (host == "bit.ly")	return proxy;
	if (host == "j.mp")		return proxy;
	if (host == "t66y.com")		return proxy;
	if (host == "twitpic.com")	return proxy;
	if (dnsDomainIs(host, "appspot.com"))	return proxy;
	if (dnsDomainIs(host, "blogimg.jp"))	return proxy;
	if (dnsDomainIs(host, "blogspot.com"))	return proxy;
	if (dnsDomainIs(host, "blogger.com"))	return proxy;
	if (dnsDomainIs(host, "facebook.com"))	return proxy;
	if (dnsDomainIs(host, "fc2.com"))		return proxy;
	//if (dnsDomainIs(host, "pixiv.net"))		return proxy;
	if (dnsDomainIs(host, "twitter.com"))	return proxy;
	//if (dnsDomainIs(host, "twimg.com"))		return proxy;
	if (dnsDomainIs(host, "vimeo.com"))		return proxy;
	if (dnsDomainIs(host, "wordpress.com"))	return proxy;
	if (dnsDomainIs(host, "youtube.com"))	return proxy;
	if (dnsDomainIs(host, "youporn.com"))	return proxy;
	
		proxy = GOAGENT;
	
	return "DIRECT";
	
}
function regExpMatch(url, pattern) {
	try { return new RegExp(pattern).test(url); } catch(ex) { return false; }
}
// shExpMatch(url, "https://api.twitter.com/*")
// regExpMatch(url, "^https?://(.+\\.)?(twitter|twimg)\\.com")
