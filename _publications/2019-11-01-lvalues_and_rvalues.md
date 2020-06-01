---
title: "Understanding Lvalues and Rvalues"
collection: publications
permalink: /publications/2019-11-01-lvalue_and_rvalue
excerpt: "<i>std::move</i><br/>`std` `standard library`"
tags:
  - std
  - c++11
  - standard library
---

# Problem

Today I'll talk about the Rvalue and Lvalue. It is 2 things that you learn very often. Some people has programmed the C++ for years and they still don't have a good understanding of RValues and LValues.
The question to ask is why do I care? Rvalue and Lvalue it is a very important concept in C++ core language. It can help you understand C++ contstruct, help you to decipher compiler errors and warnings. 
The second reason that you should care about them, that C++11 introduced a new feature called **RValue reference**. 

# The Basics

I'm giving you the simplified definition about the Rvalue and Lvalue, witch is generally accepted and it serve 99%.

** Lvalue - ** An object that occupied some identificable location in memory. It is something in memory. Not something in register! It has a identificable address.
** Rvalue - ** Any object that is not a lvalue. 

Let's look at some Lvalues examples:

{% highlight c++ %}
int i; 			//i is a lvalue
int* p = &i;	//i's address is identifiable
i = 2; 			//Memory content is modifiable

class Dog;
Dog lDog; 		//Lvalue of user defined type class
{% endhighlight  c++ %}

![](easy.gif)

Now lets we look some Rvalues examlpes:

{% highlight c++ %}
int x = 2; 			//2 is a rvalue
int x = i + 2;		//(i+2) is an rvalue
int* p = &(i+2);	//ERROR 
i+2 = 4; 			//ERROR
2 = i; 				//ERROR

Dog lDog; 		
lDog = Dog(); 		//Dog() is rvalue of user 	
{% endhighlight  c++ %}

Still clear right. So lets we look at some examples of the references or known as **lvalue references**

{% highlight c++ %}
int i;
int& r = i;
int& r = 5 			//ERROR

const int& r = 5; 	//EXCEPTION: Constant lvalue referncce can be assigned a rvalue. 
{% endhighlight  c++ %}


# Rvalue Reference


The traditional C++ rules say that you are allowed to take the address of an rvalue only if you store it in a const (immutable) variable. More technically, you are allowed to bind a const lvalue to an rvalue. Consider the following example:
{% highlight c++ %}
int& x = 666;       // Error
const int& x = 666; // OK
{% endhighlight  c++ %}


The first operation is wrong: it's an invalid initialization of non-const reference of type int& from an rvalue of type int. The second line is the way to go. Of course, being x a constant, you can't alter it.

C++0x has introduced a new type called rvalue reference, denoted by placing a double ampersand && after some type. Such rvalue reference lets you modify the value of a temporary object: it's like removing the const attribute in the second line above!

Let's play a bit with this new toy:

{% highlight c++ %}
  std::string   s1     = "Hello ";
  std::string   s2     = "world";
  std::string&& s_rref = s1 + s2;    // the result of s1 + s2 is an rvalue
  s_rref += ", my friend";           // I can change the temporary string!
  std::cout << s_rref << '\n';       // prints "Hello world, my friend"

{% endhighlight  c++ %}


Here I create two simple strings s1 and s2. I join them and I put the result (a temporary string, i.e. an rvalue) into std::string&& s_rref. Now s_rref is a reference to a temporary object, or an rvalue reference. There are no const around it, so I'm free to modify the temporary string to my needs. This wouldn't be possible without rvalue references and its double ampersand notation. To better distinguish it, we refer to traditional C++ references (the single-ampersand one) as lvalue references.

This might seem useless at a first glance. However rvalue references pave the way for the implementation of move semantics, a technique which can significantly increase the performance of your applications.
