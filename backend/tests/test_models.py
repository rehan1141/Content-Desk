import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.enums import IdeaStatus, PlatformType, ContentTypeEnum, ContentStatus, LineageType
from app.models.idea import Idea
from app.models.content import Content
from app.models.experience import Experience
from app.models.flair import Flair
from app.models.tag import Tag
from app.models.checklist import ChecklistItem
from app.models.relationship import ContentRelationship

# Setup in-memory SQLite database engine for fast ORM tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh database tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Yield a database session for testing."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_raw_idea(db):
    """Test creating a raw idea in database."""
    idea = Idea(raw_thought="I hate scripts that don't sound like me.", status=IdeaStatus.RAW)
    db.add(idea)
    db.commit()
    db.refresh(idea)

    assert idea.id is not None
    assert idea.raw_thought == "I hate scripts that don't sound like me."
    assert idea.status == IdeaStatus.RAW
    assert idea.created_at is not None


def test_idea_with_flair_and_tags(db):
    """Test associating an idea with flair and multiple tags."""
    flair = Flair(name="Opinion", color="#8b5cf6")
    tag1 = Tag(name="scripting", color="#6366f1")
    tag2 = Tag(name="personal-brand", color="#10b981")
    db.add_all([flair, tag1, tag2])
    db.commit()

    idea = Idea(
        raw_thought="Authenticity in scripting wins.",
        status=IdeaStatus.DEVELOPING,
        flair_id=flair.id
    )
    idea.tags.extend([tag1, tag2])
    db.add(idea)
    db.commit()
    db.refresh(idea)

    assert idea.flair.name == "Opinion"
    assert len(idea.tags) == 2
    tag_names = [t.name for t in idea.tags]
    assert "scripting" in tag_names
    assert "personal-brand" in tag_names


def test_idea_to_content_relationship(db):
    """Test transforming an Idea into multi-platform Content objects."""
    idea = Idea(raw_thought="Motivation isn't the problem for most students.")
    db.add(idea)
    db.commit()

    yt_content = Content(
        title="Why motivation isn't your problem",
        platform=PlatformType.YOUTUBE,
        content_type=ContentTypeEnum.YOUTUBE_VIDEO,
        status=ContentStatus.DRAFT,
        parent_idea_id=idea.id
    )
    li_content = Content(
        title="Stop searching for motivation",
        platform=PlatformType.LINKEDIN,
        content_type=ContentTypeEnum.LINKEDIN_POST,
        status=ContentStatus.DRAFT,
        parent_idea_id=idea.id
    )
    db.add_all([yt_content, li_content])
    db.commit()
    db.refresh(idea)

    assert len(idea.contents) == 2
    platforms = [c.platform for c in idea.contents]
    assert PlatformType.YOUTUBE in platforms
    assert PlatformType.LINKEDIN in platforms


def test_content_checklists_and_lineage(db):
    """Test creating checklist items and content lineage relationships."""
    source_video = Content(
        title="Moving to France for College",
        platform=PlatformType.YOUTUBE,
        content_type=ContentTypeEnum.YOUTUBE_VIDEO,
    )
    repurposed_reel = Content(
        title="3 Things I learned moving to France",
        platform=PlatformType.INSTAGRAM,
        content_type=ContentTypeEnum.INSTAGRAM_REEL,
    )
    db.add_all([source_video, repurposed_reel])
    db.commit()

    # Add checklist items to video
    step1 = ChecklistItem(title="Write script", is_completed=True, content_id=source_video.id, position=1)
    step2 = ChecklistItem(title="Record video", is_completed=False, content_id=source_video.id, position=2)
    db.add_all([step1, step2])

    # Add content lineage relationship
    lineage = ContentRelationship(
        source_content_id=source_video.id,
        target_content_id=repurposed_reel.id,
        relationship_type=LineageType.REPURPOSED_FROM
    )
    db.add(lineage)
    db.commit()

    db.refresh(source_video)
    assert len(source_video.checklists) == 2
    assert source_video.checklists[0].title == "Write script"
    assert source_video.checklists[0].is_completed is True

    # Verify lineage record
    rel = db.query(ContentRelationship).first()
    assert rel.relationship_type == LineageType.REPURPOSED_FROM
    assert rel.source_content_id == source_video.id
    assert rel.target_content_id == repurposed_reel.id
