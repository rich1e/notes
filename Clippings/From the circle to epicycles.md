---
title: "From the circle to epicycles"
source: "https://www.andreinc.net/2024/04/24/from-the-circle-to-epicycles/"
author:
published: 2024-04-24
created: 2026-07-08
description: "This article will be part of an extensive series in which I plan to explore various aspects of Fourier Mathematics. I will take notes, create some visuals (a good pretext to learn more about graphics), and hope that it will be helpful to anyone looking for a clear, visual introduction to these concepts.The article has yet to be thoroughly reviewed by anyone other than me, so I put it online, hoping to get some feedback before bringing it to a final state."
tags:
  - "clippings"
---
*... beneath a Full Moon 🌕*

This article will be part of an extensive series in which I plan to explore various aspects of [Fourier Mathematics](https://en.wikipedia.org/wiki/Fourier_analysis). I will take notes, create some visuals (a good pretext to learn more about graphics), and hope that it will be helpful to anyone looking for a clear, visual introduction to these concepts.

The article has yet to be thoroughly reviewed by anyone other than me, so I put it online, hoping to get some feedback before bringing it to a final state.

In this series, we will start with a brief recap of some of the math concepts related to the circle, including trigonometric functions like sine and cosine. We’ll also discuss Euler’s identity, introduce the concept of a sinusoid (and complex sinusoid), and finally, we’ll introduce the concept of Fourier Series.

The animations used in this series are original, although I drew inspiration from some existing materials found on the web. Please keep in mind that this is not a comprehensive course on the topic, so if you’re really interested in learning more, I recommend taking a full course on the subject.

## The Circle

It all starts with [*The Circle*](https://en.wikipedia.org/wiki/Circle):

<sup><a href="https://www.andreinc.net/js/2024-04-24-from-the-circle-to-epicycles/simplecircle.js">[simplecircle.js]</a></sup>

A circle is a geometric figure defined by its center $P(a, b)$ and its radius $r$. Algebraically, we describe it with the following equation:

$$
(x-a)^{2} + (y-b)^{2} = r^2
$$

When we set the center at the origin ($a=0, b=0$) and the radius to $r=1$, we get a special case known as [**The Unit Circle**](https://en.wikipedia.org/wiki/Unit_circle):

<sup><a href="https://www.andreinc.net/js/2024-04-24-from-the-circle-to-epicycles/simplecirclerotating.js">[simplecirclerotating.js]</a></sup>

The equation simplifies beautifully to:

$$
x^2+y^2=1
$$

One could argue *The Circle* is the epitome of [symmetry](https://en.wikipedia.org/wiki/Symmetry).

If you pick a point $A$ on the circumference and its reflection $A’$ on the opposite side, the relationship remains constant as they rotate. This rotational invariance is the “secret sauce” of Fourier Mathematics.

<sup><a href="https://www.andreinc.net/js/2024-04-24-from-the-circle-to-epicycles/triangleincircle.js">[triangleincircle.js]</a></sup>

What happens on the circle, stays on the circle. Everything is periodic, predictable, and perfectly balanced.

## The number π\\pi

In trigonometry and Fourier analysis, we rarely express angles in [degrees](https://en.wikipedia.org/wiki/Degree_\(angle\)). Instead, we use [Radians](https://en.wikipedia.org/wiki/Radian), which represent angles in relation to the number [$\pi$](https://en.wikipedia.org/wiki/Pi): $\pi$, $\frac{\pi}{2}$, $\frac{\pi}{3}$, $\frac{\pi}{4}$, and so on.

By definition, $\pi$ is the ratio of a circle’s *circumference* to its *diameter*. Regardless of the circle’s size, this ratio is constant:$\pi \approx 3.14159…$.

<sup><a href="https://www.andreinc.net/js/2024-04-24-from-the-circle-to-epicycles/rotatingpi.js">[rotatingpi.js]</a></sup>

Because of this relationship, the properties of a circle are inextricably linked to $\pi$. For any circle with a radius $r$:

- Perimeter (Circumference): $P = 2\pi r$
- Area: $A = \pi r^2$

Beyond geometry, $\pi$ is a fascinating number in its own right:

- [Irrational](https://en.wikipedia.org/wiki/Irrational_number): It cannot be expressed as a simple fraction, and its decimal representation never ends or repeats.
- [Transcendental](https://en.wikipedia.org/wiki/Transcendental_number): It is not the root of any non-zero polynomial equation with rational coefficients. (Note: Transcedental numbers are trully amazing, because first, they are truly difficult to find, and second, almost all real numbers are transcendental. The great mathematician Georg Cantor, proved that transcedental numbers are not countable).

## Radians

While we are accustomed to using degrees in daily life, the [`radian`](https://en.wikipedia.org/wiki/Radian) (or `rad`) is the standard unit for measuring angles in mathematics and physics. There is an intimate, geometric relationship between the radian and the number $\pi$:

Converting from degrees to radians is a simple matter of scaling: we multiply the angle by $\pi$, then divide the result by $180$.

In the context of Fourier Mathematics, radians are essential. They allow us to treat trigonometric functions as functions of “real numbers” rather than just “angles.” This makes the calculus involved in waves and oscillations much cleaner, without the constant need for conversion factors.

## The sine and the cosine

We can define **Sine** ($\sin$) and **Cosine** ($\cos$) through their relationship with the **Unit Circle**. Effectively, these functions act as *coordinate trackers* for a point moving around a circle:

Where:

- **$\theta$ (Theta):** The angle formed between the radius and the positive $x$ -axis.
- **The Sine ($\sin$):** Represents the vertical displacement, or the $y$ -coordinate, of the point.
- **The Cosine ($\cos$):** Represents the horizontal displacement, or the $x$ -coordinate, of the point.

Because the point eventually returns to its starting position, $\sin$ and $\cos$ are [**periodic functions**](https://en.wikipedia.org/wiki/Periodic_function) with a period of **$2\pi$**. If we “unroll” the vertical motion of the point as it rotates, it traces a perfect wave over time:

To be fair to the horizontal component, we can plot the **Cosine** on the same graph. You will notice it creates the exact same wave shape, just shifted by $\frac{\pi}{2}$ (or $90^\circ$).

## The cos⁡\\cos leads the sin⁡\\sin

When we plot $\cos$ and $\sin$ side by side, it becomes clear that they aren’t just similar—they are essentially the same wave, just operating on a different “schedule.” This difference in timing is known as a **Phase Shift**.

$$
\sin(x+\frac{\pi}{2})=\cos(x)
$$

In technical terms, we say that **$\cos$ leads the $\sin$** by $\frac{\pi}{2}$ (or $90^\circ$). If you think of the waves as racers, the cosine wave has already reached its peak by the time the sine wave is just starting to climb from zero.

This shift is the reason we describe these two as being “in quadrature.”

In Fourier analysis, having both a sine and a cosine component allows us to describe any periodic signal, regardless of its starting position (phase).

## The parity of cos⁡\\cos and sin⁡\\sin

In mathematics, [**parity**](https://en.wikipedia.org/wiki/Even_and_odd_functions) describes the symmetry of a function. A function can be classified as *even*, *odd*, or *neither*, depending on how it behaves when the sign of its input is flipped.

The *cosine* is *even*, meaning $\cos(x)=\cos(-x)$:

And the *sine* is odd, meaning $\sin(-x)=-\sin(x)$, or $\sin(x)=-\sin(-x)$:

## Complex Numbers and the Unit Circle

In the complex plane, the unit circle plays a fundamental role: every point on it corresponds to a complex number of modulus 1.

Such points admit a simple and elegant parametrization. For a real angle $\theta$, the complex number $z = \cos(\theta) + i \sin(\theta)$ lies on the unit circle and represents a rotation by angle $\theta$ from the positive real axis.

The visualization below illustrates this correspondence, showing how varying $\theta$ traces the unit circle through continuous rotation:

## Multiplying with ii is a rotation by π2\\frac{\\pi}{2}

Multiplying a *complex number* by the imaginary unit $i$ corresponds to a counterclockwise rotation by $\frac{\pi}{2}$ (90°) in the complex plane. This rotation takes place on a circle centered at the origin, whose radius is the modulus of the number:

$$
r = \lvert a + b i \rvert = \sqrt{a^2 + b^2}.
$$

Geometrically, multiplication by $i$ preserves the modulus and changes only the argument, increasing it by $\frac{\pi}{2}$.

For example, if we take a complex number $z_1 \in \mathbb{C}$ and multiply it successively by $i$, the resulting points are obtained by repeated quarter-turn rotations. After three such multiplications, $z_1$ will have visited all four quadrants of the complex plane:

## Euler’s number

The natural exponential function, usually written as $f(x) = e^x$, is a special case of the exponential function in which the base is the constant $e$, known as *Euler’s number* ($e \approx 2.71828$).

Much like $\pi$, the number $e$ is both *irrational* and *transcendental*. It can be defined in several equivalent ways, each revealing a different aspect of its behavior:

$$
e = \sum_{n=0}^{\infty} \frac{1}{n!}
  = \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!} + \cdots
$$
 
$$
e = \lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x
$$
 
$$
e = \lim_{x \to 0} (1 + x)^{\frac{1}{x}}
$$

At first glance, none of these expressions seems to have anything to do with geometry or circles. And yet, a deep connection is hiding beneath the surface.

## The exponential as an eigenfunction of differentiation

The natural exponential function has a remarkable property: it is an *eigenfunction* of differentiation. In practical terms, this means that differentiating it reproduces the same function, multiplied by a constant:

$$
\frac{d}{dx} e^{a x} = a\, e^{a x}
$$

If we now allow the constant $a$ to be imaginary and consider the function

$$
f(x) = e^{i x},
$$

its successive derivatives follow a very precise pattern:

$$
\begin{aligned}
& \frac{d}{dx} f(x)      = i\, e^{i x} \\
& \frac{d^2}{dx^2} f(x) = -\, e^{i x} \\
& \frac{d^3}{dx^3} f(x) = -\, i\, e^{i x} \\
& \frac{d^4}{dx^4} f(x) = e^{i x} = f(x)
\end{aligned}
$$

After four successive derivatives, the function returns to its original form. In a very literal sense, it has completed a *full cycle* or *full circle*.

This is exactly the same pattern we observed earlier when repeatedly multiplying a complex number by $i$.

Each multiplication by $i$ corresponds to a counterclockwise rotation by $\frac{\pi}{2}$ in the complex plane, and after four such rotations, we end up where we started.

Differentiating $e^{i x}$ plays the same role. Each derivative is equivalent to multiplying the function by $i$, so differentiation itself acts as a *rotation operator*.

## From rotation to the circle

What is a derivative, after all? It measures the rate of change of a function at a given point. But here, the rate of change of $e^{i x}$ is purely rotational. The function does not grow or shrink in magnitude; it only changes direction.

This strongly suggests a geometric interpretation: the function $e^{i x}$ traces a circle in the complex plane.

There is only one reasonable candidate. A complex-valued function with constant modulus and a linearly increasing argument must be of the form:

$$
e^{i x} = \cos(x) + i \sin(x),
$$

which is Euler’s celebrated identity.

Of course, this reasoning is intuitive rather than fully rigorous. A formal proof can be obtained by expanding $e^{i x}$, $\cos x$, and $\sin x$ into their Taylor series and comparing coefficients.

## Euler’s formula

Euler’s formula is one of the most striking identities in mathematics:

$$
e^{i x} = \cos(x) + i \sin(x)
$$

By choosing a particularly meaningful value, $x = \pi$, we obtain the famous identity

$$
e^{i \pi} + 1 = 0,
$$

which links together the fundamental constants $e$, $\pi$, $i$, 1, and 0 in a single equation.

## Sine and cosine in exponential form

If we substitute $x \rightarrow -x$ into Euler’s identity, we obtain:

$$
e^{-i x} = \cos(x) - i \sin(x)
$$

By adding and subtracting the two identities, we can isolate the cosine and sine functions and express them in exponential form:

$$
\cos(x) = \frac{e^{i x} + e^{-i x}}{2}
$$
 
$$
\sin(x) = \frac{e^{i x} - e^{-i x}}{2 i}
$$

Every point on the unit circle can therefore be described by a single complex-valued function $z(x)$, where

$$
z(x) = e^{i x} = \underbrace{\cos(x)}_{\Re(z)} + \underbrace{i \sin(x)}_{\Im(z)}.
$$

Here, the variable $x$ represents an angle $\theta \in \mathbb{R}$, so we may also write

$$
z(\theta) = e^{i \theta} = \cos(\theta) + i \sin(\theta).
$$

Throughout this article, we have freely interchanged the symbols $x$, $t$, and $\theta$. While this may seem confusing at first, it reflects an important idea: depending on context, the same parameter can be interpreted as an angle or as time.

The mathematics remains the same, the interpretation is ours to choose.

## The sinusoid

A *sinusoid*, or sine wave, is a smooth, repetitive oscillation. In physics and mathematics, it is defined by the following continuous function of time $t$.

$$
y(t) = A * \sin(2\pi ft + \varphi) = A * \sin(\omega t + \varphi)
$$

Breaking down the components of this equation:

- $A$ is called the *Amplitude*, and it’s representing the maximum deviation of the function from zero (its center value). Visually this dictates the *height* of the wave’s peaks and valleys.
- $f$ is called *ordinary frequency* and denotes the number of *complete* oscillations (or *cycles*) occurring each second. It’s typically measured in Hertz (Hz).
- $\omega=2\pi f$ is called the *angular frequency*; it’s the same thing as *ordinary frequency*, but we measure it $\frac{\text{radians}}{\text{second}}$ rather than $\frac{\text{cycles}}{\text{second}}$.
- $\varphi$ is called *phase offset*, or *phase shift*; it’s measured in radians. This determines if the oscilations begins at $t=0$. Altering the phase, you simply move the sinusoid left or right along the $x$ (horizontal) axis.

If we interpret *time* as the $x$ -axis and the signal value $y(t)$ as the $y$ -axis, the sinusoid can be written as a standard function:

$$
y=f(x)=A * \sin(\omega x + \varphi)
$$

It’s worth mentioning that the $\sin$ and $\cos$ functions are just particular cases of sinusoids. A cosine wave is mathematically identical to a sine wave, just shifted to the left by a phase offset of $\frac{\pi}{2}$ radians.

## Sinusoids are flexible

The animation below is interactive and illustrates how a sinusoid can be shaped by adjusting just a few parameters. By tweaking $A$, $\varphi$ and $\omega$ you can describe an infinite variety of oscillations, from the sound of bass guitar to the rapid alternating current powering your home. Nature oscillates!

Please choose the values of $A=$, $\omega=$ and $\varphi=$ to plot the sinusoid (if you pick $\varphi=\frac{\pi}{2}$ a cosine is plotted):

## Sinusoids can be complex

Let’s start by recalling our standard sinusoid definition:

$$
y(t) = A * sin(2\pi ft + \varphi) = A * sin(\omega t + \varphi)
$$

Bringing back Euler’s formula from the previous section, if we *scale* both sides by our amplitude $A$, we get:

$$
e^{i\theta} = \cos(\theta) + i \sin(\theta)
$$
 
$$
A*e^{i\theta}=A*(\cos(\theta)+i*\sin(\theta))
$$

Wait for it…

Now, if we substitute the static angle $\theta$ with our time-varying phase, $\theta = \omega t + \varphi$, we obtain a **complex sinusoid**:

$$
s(t)=A*e^{i(\omega t + \varphi)} = A * \cos(\underbrace{\omega t + \varphi}_{\theta}) + i * A * \sin(\underbrace{\omega t + \varphi}_{\theta})
$$

A *complex sinusoid* elegantly combines two distinct waves into a single mathematical entity. As it evolves over time, it plots a 3D corkscrew shape where:

- The **real** part behaves exactly like a cosine wave.
- The **imaginary** part behaves exactly like a sine wave.

These two components are perfectly *in sync* because they depend on the exact same rotating angle $\theta$, expressed as $\theta = \omega t + \varphi$.

Two interesting observations:

- Projecting the complex sinusoid onto the plane spanned by the Y-axis and Z-axis produces a *sine* wave (the imaginary part).
- Projecting it onto the plane spanned by the X-axis and Z-axis produces a *cosine* wave (the real part).

In this sense, a complex sinusoid can be viewed as a single rotating object whose shadows on orthogonal planes recover the familiar real-valued sinusoids, or simply put, you can have two sinusoids into one.

## Sinusoids can nullify themselves

When the peak of one sinusoid aligns with the valley of the other, they subtract from one another. At these specific points, the waves temporarily “nullify” each other, pulling the sum closer to zero. Yay!

## Adding sinusoids leads to complexity

When we combine two or more sinusoids, their values add together at every given point along the axis.

Depending on how their peaks and valleys align, they can amplify each other or completely cancel each other out, a phenomenon known as wave interference.

Let’s plot two arbitrary selected sinusoids $y_{1}(x)$ and $y_{2}(x)$, where:

- $y_{1}(x) = \frac{9}{10} * sin(7x + \frac{\pi}{2})$, and
- $y_{2}(x) = \frac{12}{10} * sin(3x - 2)$.

The sum $y(x)=y_{1}(x) + y_{2}(x)$ shows an interesting pattern

## Adding random sinusoids for fun

When we calculate and plot the sum of multiple sinuoids a complex pattern emerges. Because our two waves have different frequencies and phase offsets, they constantly drift in and out of sync with one another.

For example, we start with a simple sinusoid with ($A=1$, $\omega=1$, $\varphi=1$) and adding arbitrary sinusoids on top, leads to more and more complexity:

## A square wave and sinusoids

If we carefully choose the sinusoids and add them together, we can create predictable (geometric) patterns.

Let’s look at a classical example: building a square wave. To do this, we use the following infinite sum:

$$
y(x) =  \underbrace{\frac{4}{\pi}\sin(\omega x)}_{y_{1}(x)} + \underbrace{\frac{4}{3\pi}\sin(3\omega x)}_{y_{2}(x)} + ... + \underbrace{\frac{4}{(2k-1)\pi}{\sin((2k-1)\omega x)}}_{y_k(x)} + \dots
$$

$y_1(x), y_2(x), y_3(x), …, y_k(x), …$ are all the individual waves (sinusoids). Notice an interesting pattern: we are only adding odd frequencies, and their amplitudes are shrinking proportionally.

The magic: when we sum these smooth, continous curves together, their peaks and valleys interfere to create a “flat top” square wave. The more sinuosiuds we have in our sum, the sharper the approximation becomes.

Please choose how many sinusoids you want to use, and let’s see how the functions look like for (and $\omega$ =):

## Epicycles - First Encounter

As we established in a previous section, a single sinusoid corresponds to a point rotating around a circle!

So, instead of stacking static circles, we can chain these spinning circles together. The center of the second circle sits on the edge of the first, the third on the edge of the second, and so on. This mechanical chain is what we call a system of epicycles.

Pick and $\omega$ = to plot the circles and the corresponding $y_k(x)$ functions:

## Epicycles - An intuitive understanding

There is a beautiful, visual intuition behind why this works: because each epicycle corresponds to a specific sinusoid, combining them simply boils down to (subsequent) vector additions.

Let’s look at a concrete example. We’ll introduce three arbitrarily chosen sinusoids, each with an associated position vector (an arrow pointing from the origin to its current value):

- $y_{1}(x)=1.4sin(x + 1)$, with the associated position vector $\vec{u_{1}}$;
- $y_{2}(x)=0.8sin(2*x)$, with the associated position vector $\vec{u_{2}}$;
- $y_{3}(x)=0.5sin(3*x)$, with the associated position vector $\vec{u_{3}}$.

Their sum is:

$$
y(x) = y_{1}(x) + y_{2}(x) + y_{3}(x) = 1.4sin(x + 1) + 0.8sin(2x) + 0.5sin(3x)
$$

A position vector represents the displacement from the origin $(0, 0)$ to a specific point in space. In our case, the vector $(x, y_{k}(x))$ represents the position or location of a point on the graph of the function(s) $y_{k}(x)$ at a particular $x$ value.

If we plot $y(x)$ on the cartesian grid we obtain something like:

At any given point in time, we can say for certain that $\vec{u} = \vec{u_{1}} + \vec{u_{2}} + \vec{u_{3}}$.

## Epicycles - A flower

If we carefully pick the *right sinusoids* the moving circles can describe (approximate) any shape we want. Here is a flower for example:

Can you guess the individual sinusoids working together to draw the flower?

You probably can’t unless you apply methods from a branch of mathematics called *Fourier Analysis*.

## Fourier Series

*Fourier Series* is the mathematical process through which we expand a periodic function (with a period $P$) into an infinite sum of multiple, oscillating trigronometric functions.

To visualize this, do you remember the [Pink Floyd’s](https://en.wikipedia.org/wiki/Pink_Floyd) iconic album cover of the [*Dark Side of The Moon*](https://en.wikipedia.org/wiki/The_Dark_Side_of_the_Moon):

![](https://www.andreinc.net/images/2024-04-08-from-the-circle-to-epicycles/darksideofthemoon.jpg)

Imagine our periodic $f(x)$ is the beam of light (entering from left to right), [the prism](https://en.wikipedia.org/wiki/Prism_\(optics\)) is the *Fourier Mathematics*, and the individual spectral colors emanating from the other side are the simple trigonometric functions (sinusoids).

Following the analogy, the formula looks like this:

$$
\underbrace{f(x)}_{\text{ light itself}}=\underbrace{A_{0} + \sum_{n=1}^{\infty} [A_{n} cos(\frac{2\pi nx}{P}) + B_{n} sin(\frac{2\pi nx}{P})]}_{\text{the spectral components}}
$$

The terms $A_{0}, A_{n}$ and $B_{n}$ are called *Fourier Coefficients*, telling us exactly “how much” of the specific frequency (or *color*) is needed to reconstruct back the original wave. We compute them using the integrals:

$$
A_{0} = \frac{1}{P} \int_{- \frac{P}{2}}^{+\frac{P}{2}} f(x) dx
$$
 
$$
A_{n} = \frac{2}{P} \int_{- \frac{P}{2}}^{+ \frac{P}{2}} f(x) * \cos(\frac{2\pi nx}{P}) dx
$$
 
$$
B_{n} = \frac{2}{P} \int_{- \frac{P}{2}}^{+ \frac{P}{2}} f(x) * \sin(\frac{2\pi nx}{P}) dx
$$

## Fourier Series in Exponential Form

While sines and cosines are incredibly intuitive for visualizing waves, they can become quite cumbersome when doing heavy algebraic lifting.

By utilizing Euler’s Formula, we will convert those trigonometric functions into their exponential forms.

$$
f(x) = \sum_{n=-N}^{N} C_{n} e ^ {i2\pi \frac{n}{P}x}
$$

Notice how our index $n$ stretches into *negative territory*, this introduces the *mathematical concept* of *negative frequencies*, which is a way of dictating the direction of rotation for our complex vectors.

In this more powerful form, a simple coefficient $C_n$ replaces our previous $A_0, A_n$, and $B_n$ terms. Still, it’s defined piecewise depending on the value of $n$.

$$
C_{n} = \begin{cases}
            A_{0} & \text{if } n = 0 \\
            \frac{1}{2} (A_{n} - i * B_{n}) &  \text{if } n > 0 \\
            \frac{1}{2} (A_{n} + i * B_{n}) & \text{if } n < 0 \\
        \end{cases}
$$

Because expnentials are significantly easier to integrate than trig functions, after we peform a few algebraic substitutions, we can write a beautiful unified equation of $C_n$:

$$
C_{n} = \frac{1}{P} \int_{-\frac{P}{2}}^{\frac{P}{2}} e^{-i2\pi\frac{n}{P}x} f(x) dx
$$

## Computing the Fourier Series for the Box Function

Remember the *Square Wave* we’ve approximated with sinusoids in an earlier section? At that point, we used the following formula to express the *Square Wave* as a sum of sinusoidal components:

$$
y(x) = \frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2\pi(2k-1)fx)}{2k-1}
$$

Or, to keep things simpler, by substituting $\omega=2\pi f$ ($\omega$ is the angular frequency):

$$
y(x) = \frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)\omega x)}{2k-1}
$$

It’s time to understand how we’ve devised such an approximation.

In *isolation*, or *Square Wave Function*, $f(x)$ looks like this:

Throughout the interval $[0, 2L]$, $f(x)$ can be written as:

$$
f(x) = 2 [H(\frac{x}{L})-H(\frac{x}{L}-1)] - 1
$$

Where $H(x)$ is called the [*Heavisde Step Function*](https://mathworld.wolfram.com/HeavisideStepFunction.html) and has the following definition:

$$
H(x) =  \begin{cases}
        0 & \text{if } x \lt 0 \\
        1 & \text{if } x \ge 0 \\
        \end{cases}
$$

## Step 1 - Calculating A0A\_0

First, let’s look at $A_{0}$. Notice how we’ve shifted the interval from the standard $[-\frac{P}{2}, \frac{P}{2}]$ to $[0, 2L]$ to match our specific wave’s period:

$$
A_0 = \frac{1}{2L} \int_{0}^{2L} f(x) dx
$$

The coefficient ($A_{0}$) is just a fancy way to express the average of $f(x)$ over the interval $[0, 2L]$. In the same time, $A_{0}$ is the net area under the curve, divided by length of the interval.

If you look at the plot again, you will notice the net area to be $0$. The positive green area `(S1)` nullifies the negative red area `(S2)`, regardless of the value of $L$.

Therefore $A_0 = 0$. Yay!

## Step 2 - Calculating AnA\_n

Next, let’s compute the $A_n$ coefficients, the ones that govern the $\cos$ terms.

$$
A_{n} = \frac{1}{L} \int_{0}^{2L} f(x) * \cos(\frac{\pi nx}{L}) dx
$$

We *observe* that $f(x)$ is an *odd* function, while $\cos$ is an even function. As you might remember, the product of an *odd* function and an *even* function is an *odd* function. Because we are integrating a *odd* periodical function over a full period, the net area representing the integral will always cancel itself out. We can safely say that the $A_n$ coefficients will vanish before our eyes.

Visually speaking, regardless of how you pick $n$ or $L$, the positive and negative areas of the resulting wave will always *mirror* and destroy each other. Let’s plot the integrals for $A_1, A_2, \dots A_4$:

Similar symmetrical, self-cancelling patterns will emerge $\forall n$.

## Step 3 - Calculating BnB\_n

Finally, we need to compute the $B_n$ coefficients, the ones governing the $\sin$ terms:

$$
B_{n} = \frac{1}{L} \int_{0}^{2L} f(x) * \sin(\frac{\pi nx}{L}) dx
$$

If we plot the inner functions for $B_{1}$, $B_{2}$, $B_{3}$ and $B_{4}$ we can intuitively *feel* what’s happening with:

If you have a keen eye for geometrical representations, you will notice that for every even $n$, the red and green areas nullify each other, making the integral 0.

However, for *odd* terms, the areas add up. Because $f(x)$ and $sin(x)$ are both odd functions, their product is an even function. We can simplify our integral by taking twice the value of half the interval:

$$
B_{n} = 2 * [\frac{1}{L} \int_{0}^{L} f(x) * \sin(\frac{\pi nx}{L}) dx]
$$

Since $f(x)=1$ on $[0, L]$, this is standard integration. We can perform [u-substition](https://en.wikipedia.org/wiki/Integration_by_substitution) to solve it:

$$
B_{n} = \frac{2}{L} \int_{0}^{nL\pi} \frac{\sin(\frac{u}{L})}{n\pi}du
$$

After we take the constant out, we compute the integral, use the intervals, and take into consideration the periodicity of cosine:

$$
B_{n} = \frac{2}{n\pi}(1-(-1)^n)
$$

## Step 4 - Putting all together

Putting the calculated coefficients back into the *master* formula for the *Fourier Series*:

$$
f(x)=\underbrace{A_{0}}_{0} + \sum_{n=1}^{\infty} [\underbrace{A_{n} \cos(\frac{\pi nx}{L})}_{0} + B_{n} \sin(\frac{\pi nx}{L})]
$$

Since only the odd terms of $B_n$ *survive*, the series become:

$$
f(x)=\frac{4}{\pi} \sum_{n=1,3,5...}^{+\infty} (\frac{1}{n} * \sin(\frac{\pi nx}{L}))
$$

To *clean up* the index so we can *count normally*, consider substituting $n \rightarrow 2k-1$ and consider:

$$
f(x)=\frac{4}{\pi} \sum_{k=1}^{+\infty} (\frac{\sin(\frac{\pi (2k-1)x}{L})}{(2k-1)})
$$

Finally, we substitute $L \rightarrow \frac{1}{2f}$, and $2\pi f \rightarrow \omega$ to arrive at the initial (and final) formula:

$$
f(x) = \frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)\omega x)}{2k-1}
$$

In real life, we can’t actually sum to infinity. We have to stop at some finite number $n$, so let’s call our approximation $s(x)$:

$$
s(x) = \frac{4}{\pi}\sum_{k=1}^{n}\frac{\sin((2k-1)\omega x)}{2k-1} \approx f(x)
$$

In the next animation, you will see that by increasing $n$, the accuracy of our approximation gets better and better, and the *gaps* are slowly closed:

To truly understand how adding more coefficients improves the approximation of the shape, let’s look at the first 5 individual terms $s_{1}(x)$, $s_{2}(x)$, $s_{3}(x)$, $s_{4}(x)$ and $s_{5}(x)$ (we will pick $\omega=\frac{\pi}{2}$, so that $2L=1$):

$$
s_{1}(x) = \frac{4}{\pi} \sin(\frac{\pi x}{2})
$$
 
$$
s_{2}(x) = \frac{4}{3\pi} \sin(\frac{3\pi x}{2})
$$
 
$$
s_{3}(x) = \frac{4}{5\pi} \sin(\frac{5\pi x}{2})
$$
 
$$
s_{4}(x) = \frac{4}{7\pi} \sin(\frac{7\pi x}{2})
$$
 
$$
s_{5}(x) = \frac{4}{9\pi} \sin(\frac{9\pi x}{2})
$$

Each term is a simple sinusoid, with rapidly shirinking amplitudes and increasing frequencies.

So, if we were to approximate a *Square Wave* with its fifth partial sum (the red dot), we would obtain something like this:

Notice how *obsessed* the *red dot* is with the *blue dot* (the actual Square Wave function) and how closely it tries to follow it.

We can always add more terms to the partial sum to help the *red dot* in its *holy mission*, improving the approximation until nobody cares anymore.

## Example - The Fourier Series of the Triangle wave

Without going into the heavy integration math this time, let’s look straight at the Fourier Series decomposition for a triangle wave:

$$
s(x)=\frac{8}{\pi^2}\sum_{k=1}^{N}\frac{(-1)^{k-1}}{(2k-1)^2}*\sin((2k-1)x)
$$

Plotting the function $s(x)$, we will see that things converge smoothly and fast. By the time $n$ approaches $6$, the triangle shape is getting clear:

Let’s compute and expand the first terms six terms of the $\sum$, so that:

$$
s(x) \approx s_1(x) + s_2(x) + s_3(x) + s_4(x) + s_5(x) + s_6(x)
$$

Breaking down each term:

$$
s_1(x)=\frac{8}{\pi^2} \cdot \sin(x)
$$
 
$$
s_2(x)=-\frac{8}{3^2\pi^2} \cdot \sin(3x)
$$
 
$$
s_3(x)=\frac{8}{5^2\pi^2} \cdot \sin(5x)
$$
 
$$
s_4(x)=-\frac{8}{7^2\pi^2} \cdot \sin(7x)
$$
 
$$
s_5(x)=\frac{8}{9^2\pi^2} \cdot \sin(9x)
$$
 
$$
s_6(x)=-\frac{8}{11^2\pi^2} \cdot \sin(11x)
$$

A keen eye will see will observe the that $s_2(x)$, $s_4(x)$, $s_6(x)$ and all the even terms are *negative*.

But a negative amplitude doesn’t make much intuitive sense, at least not physically. You can’t draw a circle with a negative radius! So, what are we going to do with that minus sign?

Because of trigonometric identities, we have two options to rewrite it:

1. Because $\sin(-x)=-\sin(x)$, nobody stops us to make the *frequency* negative. For example, $s_2(x)=\frac{8}{3^2\pi^2}*\sin(-3x)$, so that the $\omega=-3$. But again, why would we want a *negative frequency*? Outside of complex exponentials, this also lacks physical intuition.
2. We can use $\vert A \vert$ and shift the signal with $\pi$, so that $\varphi=\pi$.

In practice, we go with option 2. It is far more practical and gives us better geometric control.

$$
s_2(x)=-\frac{8}{3^2\pi^2}*\sin(3x)
$$
 
$$
s_2(x)=\frac{8}{3^2\pi^2}*\sin(3x + \pi)
$$

Visually speaking, the results are identical. If we plot $sin(-x)$ and $sin(x+\pi)$ side by side the two overlap:

Taking this phase shift into consideration, the negative terms of $s(x)$ approximation neatly become positive amplitudes with $\pi$ phase offset:

- $s_2(x)=\frac{8}{3^2\pi^2}*sin(3x+\pi)$;
- $s_4(x)=\frac{8}{7^2\pi^2}*sin(7x+\pi)$;
- $s_6(x)=\frac{8}{11^2\pi^2}*sin(11x+\pi)$;
- …and so on

## Example - The Fourier Series of a Sawtooth Function

Shamelessly skipping the math demonstration, a reverse-sawtooth function has the following form:

$$
s(x)=\frac{2}{\pi}\sum_{k=1}^{N}(-1)^k*\frac{\sin(kx)}{k}
$$

Plotting $s(x)$, while increasing $n$, things look like this:

## The Fourier Series Machinery

Instead of looking at static equations, let’s watch how these mathematical terms translate into physical motion to create practical, predictable patterns.

You can pick the shape of the desired signal from here: and the sketch will change accordingly.

What you are looking at is essentially a bunch of spinning circles chained tip-to-tail on a stick. However, every single part of this visual mechanism corresponds directly to the variables in our Fourier equations:

- The radius of each circle represents the amplitude $A$;
- The speed at which each circle rotates represents the angular frequency $\omega$;
- The initial angle of the “stick” inside the circle at $t=0$ represents the phase offset $\varphi$.
![](https://www.andreinc.net/images/2024-04-08-from-the-circle-to-epicycles/fmachinery.jpg)

Isn’t it amazing? The complex, jagged, sharp-edged waveforms that power our modern digital world can all be reverse-engineered down to a beautifully simple concept: a bunch of perfectly smooth, spinning circles on a stick.