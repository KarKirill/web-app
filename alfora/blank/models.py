from django.db import models # type: ignore

class FileSave(models.Model):
  file_passport = models.FileField(upload_to = 'upldfile/passport/', null=True, blank=True)
  file_snils = models.FileField(upload_to = 'upldfile/snils/', null=True, blank=True)
  file_lvplc = models.FileField(upload_to = 'upldfile/live_place/', null=True, blank=True)

class Clinic(models.Model):
  """Клиника"""

  class Meta:
    db_table = "clinic"
    verbose_name = "Клиника"
    verbose_name_plural = "Клиника"

  snils = models.TextField(verbose_name="СНИЛС")
  surname = models.TextField(verbose_name="Фамилия")
  name = models.TextField(verbose_name="Имя")
  middle_name = models.TextField(verbose_name="Отчество")
  date_of_birth = models.TextField(verbose_name="Дата рождения")
  place_of_birth = models.TextField(verbose_name="Место рождения")
  gender = models.TextField(verbose_name="Пол")
  passport_place = models.TextField(verbose_name="Место выдачи паспорта")
  passport_date = models.TextField(verbose_name="Дата выдачи паспорта")
  departament_code = models.TextField(verbose_name="Код подразделения")
  place_of_residence = models.TextField(verbose_name="Место жительства")
  passport = models.TextField(verbose_name="Серия и номер паспорта")

  def __str__(self):
    return f"ФИО: {self.surname} {self.name} {self.middle_name}, Пол: {self.gender}, Дата рождения: {self.date_of_birth}, Дата выдачи паспорта: {self.passport_date}, Место выдачи паспорта: {self.passport_place}, Код подразделения: {self.departament_code}, Место жительства: {self.place_of_residence}, СНИЛС: {self.snils}, Паспорт: {self.passport}"