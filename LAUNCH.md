# Launching specialgreenbr.com

Three things happen outside this repository. They need a login, so they are yours to do.
Everything else is done and waiting.

---

## 1. Cloudflare DNS

**You are not getting anything from Cloudflare.** Cloudflare is only where the records get
typed. The values below are GitHub Pages' own server addresses, the same for every site
hosted there, published in GitHub's documentation. Nothing here is unique to us.

### Where to click

1. Sign in at **dash.cloudflare.com**
2. Click **specialgreenbr.com** in the site list
3. Left sidebar → **DNS** → **Records**
4. Delete any existing `A` or `CNAME` record on `@` or on `www`. A leftover record from the
   registrar's parking page will quietly win and nothing will work.
5. **Add record**, five times:

| Type | Name | IPv4 address / Target | Proxy status |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | **DNS only** |
| A | `@` | `185.199.109.153` | **DNS only** |
| A | `@` | `185.199.110.153` | **DNS only** |
| A | `@` | `185.199.111.153` | **DNS only** |
| CNAME | `www` | `markbalangodoy.github.io` | **DNS only** |

`@` means the bare domain. Cloudflare may display it as `specialgreenbr.com` once saved.

### The two traps

Both of these are the difference between working and mysteriously broken.

**Proxy must be OFF.** The toggle in the proxy column must be a **grey cloud**, not orange.
Cloudflare's proxy sits in front of the site and prevents GitHub from issuing the HTTPS
certificate. The site will appear broken with no useful error. Once the certificate has been
issued you can switch the proxy back on if you want Cloudflare's caching.

**SSL/TLS mode must be Full.** Left sidebar → **SSL/TLS** → **Overview** → select **Full**.
If it is set to **Flexible**, visitors get an endless redirect loop. This is the single most
common Cloudflare and GitHub Pages failure and it looks nothing like a DNS problem.

### Then, in GitHub

1. Go to the repository → **Settings** → **Pages**
2. **Custom domain**: `specialgreenbr.com` → **Save**
   (The `CNAME` file is already committed, so this may already be filled in.)
3. Wait for the green tick, then tick **Enforce HTTPS**

The HTTPS box stays greyed out until the certificate is issued. That is usually a few
minutes and occasionally an hour. It is not stuck; it is waiting on DNS to propagate.

---

## 2. The Web3Forms key

This is what makes the estimate form actually send. Roughly a minute.

1. Go to **web3forms.com**
2. Enter **specialgreenllc@gmail.com** in the box on the front page
3. They email an **access key** to that address, a long string of letters and numbers
4. Send the key over and it goes into `index.html`

The key is a public submit key, not a password. It is designed to sit in page source and it
cannot be used to read anything. There is no account to create and the free tier covers far
more than this site will ever send.

**Until the key is in, the form does not pretend.** It tells the visitor to call, keeps
everything they typed on screen, and never shows a success message it did not earn. It looks
slightly unfinished, which is the correct trade against losing a job.

---

## 3. Reviews and attributions

- **Google reviews**: paste the text, the name as it appears on Google, and the location.
  Three or four is plenty. Do not reword them: a slightly awkward real review reads as real,
  a polished one reads like marketing. Until they arrive the section does not exist on the
  page at all, which is the intended fail-safe.
- **Two pull quotes** are still marked *"Attribution to confirm"*, one in the crew section and
  one in the customer band. They need a name against them or they come out.

---

## 4. The flip, which is mine

Once the domain resolves over HTTPS, one commit does the rest:

- `noindex,nofollow` removed from `index.html` and from the guide pages
- `robots.txt` opened up and pointed at the sitemap
- staging banner and the photo-slot toggle removed
- sitemap submitted to Google Search Console

**Order matters.** None of that happens before DNS resolves. Removing `noindex` while the
site still answers on `markbalangodoy.github.io` invites Google to index the wrong host, and
then the real domain spends months competing with its own staging copy.
