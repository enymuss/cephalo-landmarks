"""Add Meausurement model

Revision ID: c04fc87e87fc
Revises: 1276f064b13a
Create Date: 2021-02-09 12:49:49.212588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04fc87e87fc'
down_revision = '1276f064b13a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cephalo_measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_name', sa.String(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('cephalo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cephalo_id'], ['cephalo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cephalo_measurement_id'), 'cephalo_measurement', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cephalo_measurement_id'), table_name='cephalo_measurement')
    op.drop_table('cephalo_measurement')
    # ### end Alembic commands ###
