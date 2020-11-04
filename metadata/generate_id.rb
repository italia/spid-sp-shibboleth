#!/usr/bin/env ruby

allowed_chars = Range.new('a','f').to_a + Range.new('0','9').to_a
id = "_" + 43.times.map{ allowed_chars[Random.rand(16)] }.join
puts id
