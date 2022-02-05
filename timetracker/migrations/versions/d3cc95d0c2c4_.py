"""empty message

Revision ID: d3cc95d0c2c4
Revises: b281d5e6fcf7
Create Date: 2021-11-28 12:15:36.580629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3cc95d0c2c4'
down_revision = 'b281d5e6fcf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('assignee', sa.String(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assignee'], ['employees.emp_id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
