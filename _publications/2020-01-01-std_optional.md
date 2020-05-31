---
title: "How should one use std::optional?"
collection: publications
permalink: /publications/2020-01-01-std_optional
excerpt: "<i>std::optional</i><br/>`std` `c++17` `standard library` `functional programming`"
tags:
  - std
  - c++11
  - standard library
  - std::optional
---

# Problem

Today we're gonna be looking the std::optional for those that who aren't use std::optional yet. I will try to show you a little bit why it is usefull and how you can use it. But those of you who are already in the know about the std::optional maybe I can show you a few additional applications you might not have thought.

So question is why you want this std::optional? Usually, you can use if you want to represent a nullable type nicely, Return a result of some computation (processing) that fails to produce a value and is not an error, or perform lazy-loading of resources. It is messy? Let me show you on the example. Let's we load the file.


# The Basics

I know, many readers say that I know the solution.

{% highlight c++ %}
std::string LoadFile()
{
	std::ifstream file{"test.txt"};
	if(file)
	{
		return std::string {
			std::istreambuf_iterator{ file}, 
			std::istreambuf_iterator<char>{ }
		}
	}
	return {};
};
{% endhighlight  c++ %}


So the LoadFile function's job is open the ".txt" file and return with the string with file content. If the file doesn't exist then return with a default contructed empty string. If successfully open the file, we use the iterrators into the file stream and we just fill the string with iterators very quickly and very cleanly. 

So let's call our function. 

{% highlight c++ %}
int main()
{
	const auto s = LoadFile();
	if(s.empty())
	{
		std::cout << "File test.txt could not be opened!" << std::endl; 
	}
	else
		std::cout << s.
}
{% endhighlight  c++ %}


It look all fine? Right?
If the file don't exist we got the error message. Otherwise we print the file's content. But did you tried with the empty "test.txt" file?

If you don't try it, i tell you the answer. We get

{% highlight c++ %}
>> "File test.txt could not be opened!" message.
{% endhighlight  c++ %}


But it is not true! The file could be opened, just there was nothing in it. 
So the problem here that we're returning a value of the string that means there is no file. There is possible to have a files that are empty. 

###I know, many readers say that I know the solution. "std::pair<bool, std::string>" 

{% highlight c++ %}
std::pair<bool, std::string> LoadFile()
{
	std::ifstream file{"test.txt"};
	if(file)
	{
		return { true, std::string {
			std::istreambuf_iterator{ file}, 
			std::istreambuf_iterator<char>{ } }
	}
	return {false, {}};
};
{% endhighlight  c++ %}

So now we are handling all cases. If the file don't exist we got the error message. Otherwise we print the file's content and if the file is empty than we get the empty string.
But this solution is a little bit clunky. You have to remember that the first bool means exist the file, the second means file content. 
###It is not a self descriptive solution :(


# std::optional

Let me show you, what it is the sexy solution. std::optional<std::string>. We are returning with the string by value, but it is optional. It may or may not be there. 


{% highlight c++ %}
std::optional<std::string> LoadFile()
{
	std::ifstream file{"test.txt"};
	if(file)
	{
		return std::string {
			std::istreambuf_iterator{file}, 
			std::istreambuf_iterator<char>{ } }
	}
	return {};
}


int main()
{
	std::cout << LoadFile().value_or("File test.txt could not be opened!") << std::endl;
	return 0;
}
{% endhighlight  c++ %}


Simple, readable and sexy solution. 

Thank you for reading!

* Sources:
    * [https://dzone.com/articles/using-c17-stdoptional](https://dzone.com/articles/using-c17-stdoptional)
    * [https://en.cppreference.com/w/cpp/utility/optional](https://en.cppreference.com/w/cpp/utility/optional)
