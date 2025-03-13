from model import session, Page, Post, Comment

# Create sample page
page = Page(
    linkedin_id="12345",
    name="Tech Insights",
    url="https://linkedin.com/company/tech-insights",
    profile_picture="https://example.com/logo.png",
    description="A page about tech trends.",
    website="https://techinsights.com",
    industry="Technology",
    followers=50000,
    headcount=200,
    specialties="AI, Cloud, Software Development"
)

post = Post(
    page=page,
    content="Exciting new trends in AI for 2025!",
    post_url="https://linkedin.com/posts/123",
)

comment = Comment(
    post=post,
    user_name="John Doe",
    content="This is very insightful!",
)

session.add(page)
session.commit()
print("Sample data added successfully!")
