from flask_sqlalchemy import SQLAlchemy, model

# Overrriding base class


class Model(model.Model):

    def insert(self):

        try:
            db.session.add(self)
            db.session.commit()
            return self.format()
        except Exception as e:
            print('error: ', e)
            db.session.rollback()
            return None
        finally:
            db.session.close()

    def format(self):
        dic = vars(self)
        dic.pop('pass_hash', None)
        return dic

    def update(self):

        try:
            db.session.commit()
        except Exception as e:
            print('error: ', e)
            error = True
            db.session.rollback()
            return error
        finally:
            db.session.close()

    def delete(self):
        error = False
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print('error: ', e)
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        return error


db = SQLAlchemy(model_class=Model)
