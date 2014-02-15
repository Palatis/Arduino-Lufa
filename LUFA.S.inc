/*
 * Include this file in one of your project's c source file.
 * For example, create a file named "LUFA.S" and include this.
 * === LUFA.c ===
 * #include "LUFAConfig.h"
 * #include <LUFA.S.inc>
 * ==============
 */
 
#ifndef __LUFA_S__
#define __LUFA_S__

#if (ARCH == ARCH_UC3)
# include <LUFA/Platform/UC3/Exception.S>
#endif

#endif