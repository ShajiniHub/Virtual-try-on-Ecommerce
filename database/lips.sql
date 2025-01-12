-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 05, 2024 at 12:10 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `lips`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `pro_username` varchar(30) NOT NULL,
  `color` varchar(40) NOT NULL,
  `price` varchar(20) NOT NULL,
  `req_date` varchar(20) NOT NULL,
  `username` varchar(30) NOT NULL,
  `quantity` varchar(30) NOT NULL,
  `total` varchar(20) NOT NULL,
  `payment` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`id`, `name`, `mobile`, `email`, `pro_username`, `color`, `price`, `req_date`, `username`, `quantity`, `total`, `payment`) VALUES
(1, 'Lab', 7267282728, 'exsanple74@gmail.com', 'lokesh', '#ff0000', '560', 'May 14, 2024', 'lokesh', '2', '1120.0', 'UPI'),
(2, 'Lab', 7267282728, 'exsanple74@gmail.com', 'lokesh', '#ff0000', '560', 'May 14, 2024', 'lokesh', '2', '1120.0', ''),
(3, 'Lab', 7267282728, 'exsanple74@gmail.com', 'lokesh', '#ff0000', '560', 'May 20, 2024', 'lokesh', '2', '1120.0', 'UPI'),
(4, 'Lab', 7267282728, 'exsanple74@gmail.com', 'lokesh', '#ff0000', '560', 'May 20, 2024', 'lokesh', '2', '1120.0', 'UPI');

-- --------------------------------------------------------

--
-- Table structure for table `cc_data`
--

CREATE TABLE `cc_data` (
  `id` int(11) NOT NULL,
  `input` varchar(200) NOT NULL,
  `output` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_data`
--

INSERT INTO `cc_data` (`id`, `input`, `output`) VALUES
(1, 'Hi, Hello', 'Hello How Can I Assist You !'),
(2, 'What is the best way to apply lipstick?', '1.Start with exfoliated lips. Use a lip scrub or a soft toothbrush to remove dead skin.2.Apply a lip balm to moisturize and smooth your lips.3.Use a lip liner to define your lips and prevent feathering.4.Apply lipstick starting from the center of your lips and moving outward.5.Blot your lips with a tissue and reapply for longer-lasting color.'),
(3, 'How can I make my lipstick last longer?', '1.Exfoliate and moisturize your lips before applying lipstick.2.Use a lip primer or a bit of foundation on your lips.3.Apply lip liner over your entire lips, not just the edges.4.Apply your lipstick, blot with a tissue, and then apply a second layer.5.Set with a translucent powder for extra staying power.'),
(4, 'How do I choose the right lipstick shade for my skin tone?', '1.For fair skin, try light pinks, nudes, and coral shades.2.For medium skin, opt for rose, mauve, and berry shades.3.For olive skin, go for peach, warm reds, and bronze shades.4.For dark skin, rich reds, deep purples, and browns look great. Remember, the best shade is the one that makes you feel confident!'),
(5, 'What is the difference between matte and glossy lipstick?', 'Matte Lipstick: Has a flat, non-shiny finish. It''s long-lasting and highly pigmented but can be drying.\r\nGlossy Lipstick: Has a shiny, wet look. It''s moisturizing and makes lips look fuller, but it may not last as long and can transfer more easily.'),
(6, 'Can I wear lipstick if I have dry lips?', '1.Exfoliate your lips gently to remove flakes.2.Use a hydrating lip balm before applying lipstick.3.Choose moisturizing lipstick formulas, such as creamy or satin finishes.4.Avoid matte lipsticks, as they can be drying.'),
(7, 'How do I prevent my lipstick from smudging?', '1.Apply a lip primer or foundation on your lips.2.Use a lip liner to outline and fill in your lips.3.Apply your lipstick in thin layers, blotting between each layer.4.Set your lipstick with a translucent powder.5.Avoid touching your lips and eating greasy foods.'),
(8, 'What is liquid lipstick and how is it different from regular lipstick?', 'Liquid lipstick comes in a liquid form and is applied with a wand. It dries down to a matte or satin finish and tends to be more long-lasting than regular lipstick. Regular lipstick is typically in solid form and may come in various finishes like matte, satin, or glossy. Liquid lipstick can be more drying, so ensure your lips are well-prepped before application.'),
(9, 'Can I use lipstick as blush?', 'Yes, you can use lipstick as blush. Apply a small amount of lipstick to the back of your hand, then use your fingers or a makeup sponge to dab it onto your cheeks. Blend it out for a natural flush of color.'),
(10, 'What should I do if my lipstick breaks?', '1.Gently heat the broken ends with a lighter or match until slightly melted.2.Press the broken pieces together and smooth the seam.3.Place the lipstick in the refrigerator for a few hours to set.'),
(11, 'Are there any tips for applying dark lipstick?', '1.Exfoliate and moisturize your lips.2.Use a lip liner that matches your lipstick to outline and fill in your lips.3.Apply the lipstick with a lip brush for precise application.4.Clean up any edges with a concealer brush and concealer.5.Blot with a tissue and reapply for intense color.'),
(12, 'Can I wear lipstick with lip gloss?', 'Yes, you can layer lipstick with lip gloss for added shine. Apply lipstick first, blot gently with a tissue, and then apply lip gloss to the center of your lips for a fuller look.'),
(13, 'What are some tips for choosing a red lipstick?', '1.Cool-Toned Skin: Opt for blue-based reds.2.Warm-Toned Skin: Choose orange-based or coral reds.3.Neutral Skin: Go for true reds that aren''t too warm or cool.4.Consider your undertones and the occasion when selecting the intensity (bold vs. subtle) of red.'),
(14, 'How can I make my lipstick look more natural?', '1.Choose a shade close to your natural lip color.2.Use a lip liner that matches your lips to define the edges.3.Apply lipstick with your finger for a softer, diffused effect.4.Blot with a tissue to remove excess product and blend.'),
(15, 'Is it necessary to use a lip liner?', '1.Define the shape of your lips.2.Prevent lipstick from feathering or bleeding.3.Extend the wear time of your lipstick.'),
(16, 'What should I do if my lipstick color doesn''t look right on me?', '1.Try mixing shades to create a custom color.2.Consider your outfit and overall makeup look.3.Experiment with different finishes (matte, satin, glossy).4.Visit a makeup counter for professional advice.'),
(17, 'What is the shelf life of lipstick?', 'The shelf life of lipstick is typically 1-2 years. Check the packaging for the expiration date symbol (an open jar icon with a number indicating the number of months the product is good after opening).');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `file` varchar(100) NOT NULL,
  `favcolor` varchar(100) NOT NULL,
  `price` varchar(20) NOT NULL,
  `reg_date` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `pname` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `file`, `favcolor`, `price`, `reg_date`, `username`, `pname`) VALUES
(1, 'work-1.jpg', 'Plussy blue', '560', '2024-05-14', 'lokesh', ''),
(2, 'images.jpg', 'red', '560', '2024-06-06', 'admin', ''),
(3, '1.jpg', 'Black', '560', '2024-06-06', 'admin', '');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `id` int(11) NOT NULL,
  `request` varchar(300) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `username` varchar(30) NOT NULL,
  `date` varchar(20) NOT NULL,
  `status` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `request`
--

INSERT INTO `request` (`id`, `request`, `mobile`, `email`, `username`, `date`, `status`) VALUES
(1, 'I have to buy a eyeliner', '8838468320', 'exsanple74@gmail.com', 'lokesh', 'June 13, 2024', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `reg_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `mobile`, `email`, `username`, `password`, `reg_date`) VALUES
(1, 'Lab', 8838468320, 'exsanple74@gmail.com', 'lokesh', '1234', '2024-05-14');
