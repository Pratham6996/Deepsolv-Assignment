from model import session, Page, Post, Comment

# Query Pages
pages = session.query(Page).all()
for p in pages:
    print(f"Page: {p.name}, Followers: {p.followers}")

# Query Posts
posts = session.query(Post).all()
for post in posts:
    print(f"Post: {post.content}, URL: {post.post_url}")

# Query Comments
comments = session.query(Comment).all()
for comment in comments:
    print(f"Comment by {comment.user_name}: {comment.content}")
