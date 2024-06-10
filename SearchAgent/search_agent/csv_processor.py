import pandas as pd

class CSVProcessor:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def process_csv(self):
      data = pd.read_csv(self.input_file)
      data = data.dropna()

      selected_columns = ['name', 'description', 'tags', 'representativeName', 'professor', 'googleScholarUrl', 'numPostDoc', 'numPhd', 'numMaster', 'numUnderGraduate', 'campus']
      selected_df = data[selected_columns]

      def create_sentence(row):
          return f"이 랩실 이름은 {row['name']}이야. {row['professor']} 교수님이 담당하시는 연구실이고 {row['description']} {row['campus']}에 위치해있고 현재 연구실에는 postdoc은 {row['numPostDoc']} 명, 박사 과정 학생은 {row['numPhd']} 명, 석사 과정 학생은 {row['numMaster']} 명, 학부연구생(인턴)은 {row['numUnderGraduate']} 명이야."

      selected_df['combined_info'] = selected_df.apply(create_sentence, axis=1)

      selected_df[['combined_info']].to_csv(self.output_file, index=False)
      

class CSVProcessor_lab:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def process_csv(self):
      data = pd.read_csv(self.input_file)
      data = data.dropna()

      selected_columns = ['name', 'description', 'tags', 'representativeName', 'numMembers', 'location']
      selected_df = data[selected_columns]

      def create_sentence(row):
          return f"이 동아리 이름은 {row['name']}이야. {row['representativeName']}이 담당하시는 동아리고 {row['description']}. {row['location']}에 위치해있고 현재 동아리 인원은 {row['numMembers']} 명이야."

      selected_df['combined_info'] = selected_df.apply(create_sentence, axis=1)

      selected_df[['combined_info']].to_csv(self.output_file, index=False)
      
