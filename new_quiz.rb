#! /usr/bin/env ruby

require 'fileutils'
require 'json'

template = 'quiz_template'
assessments_dir = '../../courseInstances/Fa23/assessments'

if (! File.exist?(template)) 
  $stderr.puts("No template directory found. Are you in the quiz directory?")
  exit
end


if (ARGV.length < 1) 
  $stderr.puts "Usage: new_quiz.rb name"
  exit
end

full_name = ARGV[0]
if full_name =~ /^([^_]+)_(.*)/
  category = $1
  name = $2
  puts "Creating #{full_name} in category #{category} with name #{name}"
else
  $stderr.puts "quiz question name =>#{full_name}<= is not of the correct format (foo_bar)"
  exit
end

quiz_name = nil
if (ARGV.length > 1) 
  quiz_name = ARGV[1]
  if quiz_name =~ /^quiz(.+)/
    quiz_number = $1
  else
    $stderr.puts "quiz name =>#{quiz_name}<= is not of the correct format (quizFoo)"
    exit
  end
  puts "Also creating quiz named #{quiz_name}"
end


dir_name = "#{category}/#{full_name}"

if (File.exist?(dir_name))
  $stderr.puts "directory #{dir_name} already exists."
  exit
end

#
# Set up question
#

notebook_file = "learning_target.ipynb"

FileUtils.cp_r(template, dir_name)

info = JSON.parse File.read "#{dir_name}/info.json"
info['uuid'] = `uuidgen`.chomp
File.write("#{dir_name}/info.json", JSON.pretty_generate(info))

tests = File.read "#{dir_name}/tests/test.py"
tests.gsub!('zzCODE_FILEzz', notebook_file)
File.write("#{dir_name}/tests/test.py", tests)

#
# Set up assignment
#

unless quiz_name.nil?
  FileUtils.mkdir "#{assessments_dir}/#{quiz_name}"
  info = JSON.parse File.read "#{assessments_dir}/infoQuizTemplate.json"
  info['uuid'] = `uuidgen`.chomp
  info['title'] = "Quiz #{quiz_number}"
  info['number'] = quiz_number
  info['zones'].first['questions'].first['id'] = "quiz/#{dir_name}"
  info['zones'].first['questions'].first['points'] = 100
  info['zones'].first['questions'].first['maxPoints'] = 100
  File.write("#{assessments_dir}/#{quiz_name}/infoAssessment.json", JSON.pretty_generate(info))
end