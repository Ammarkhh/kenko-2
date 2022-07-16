# Generated by Django 3.2 on 2022-05-09 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('calories', models.DecimalField(blank=True, decimal_places=2, help_text='Calories for this ingredient per 1g', max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('video', models.CharField(blank=True, max_length=300, null=True)),
                ('instructions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.ingredient')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.meal')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.ManyToManyField(through='nutrition.MealIngredient', to='nutrition.Ingredient'),
        ),
        migrations.CreateModel(
            name='Macro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('macro_type', models.CharField(choices=[('FAT', 'Fats'), ('PRO', 'Proteins'), ('CAR', 'Carbohydrates')], default='FAT', max_length=3)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='How much of this macro is in the ingredient per gram', max_digits=6, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrition.ingredient')),
            ],
            options={
                'unique_together': {('macro_type', 'ingredient')},
            },
        ),
    ]
