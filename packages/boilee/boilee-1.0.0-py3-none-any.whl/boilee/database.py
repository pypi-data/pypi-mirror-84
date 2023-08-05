from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Boilerplate(Base):
    __tablename__ = "boilerplates"

    name = Column(String, primary_key=True)
    docopt_string = Column(String, nullable=False)
    inquirer_questions = Column(String, nullable=False)
    structure = Column(String, nullable=False)

    paths = relationship("Path")


class Path(Base):
    __tablename__ = "paths"

    id = Column(Integer, primary_key=True)
    boilerplate_name = Column(Integer, ForeignKey("boilerplates.name"), nullable=False)
    path = Column(String, nullable=False)
    content = Column(String)
    is_plain_text = Column(Boolean, nullable=False)

    boilerplate = relationship("Boilerplate")


class Database:
    def __init__(self, directory=""):
        if not directory:
            self.path = "database.sqlite"
        elif not directory.startswith("/"):
            self.path = f"/{directory}/database.sqlite"
        else:
            self.path = f"{directory}/database.sqlite"

        engine = create_engine(f"sqlite:///{self.path}")

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def commit(self, line_object):
        self.session.add(line_object)
        self.session.commit()

    def add_boilerplate(self, **args):
        new_boilerplate = Boilerplate(**args)

        return new_boilerplate

    def add_path(self, **args):
        new_path = Path(**args)

        return new_path

    def get_boilerplate(self, boilerplate_name):
        boilerplate = self.session.query(Boilerplate).get(boilerplate_name)

        return boilerplate

    def get_paths(self, boilerplate):
        paths = (
            self.session.query(Path)
            .filter(
                Path.boilerplate == boilerplate,
                Path.is_plain_text == True,
            )
            .all()
        )

        paths = {path.path: path.content for path in paths}

        return paths

    def get_binary_paths(self, boilerplate_name):
        paths = (
            self.session.query(Path)
            .filter(
                Path.boilerplate_name == boilerplate_name,
                Path.is_plain_text == False,
            )
            .all()
        )

        paths = [path.path for path in paths]

        return paths
