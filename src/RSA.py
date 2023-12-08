
import random

#=========================================================================================#
# Fuction: gcd(a, b)                                                                      #
#    - a : an integer                                                                     #
#    - b : an integer                                                                     #
# Returns the greatest common divisor of a and b                                          #
#=========================================================================================#
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#=========================================================================================#
# Fuction: get_d(e, z)                                                                    #
#    - e : the integer exponent                                                           #
#    - z : the integer (p-1)(q-1)                                                         #
# Returns the corresponding d value                                                       #
#=========================================================================================#
def get_d(e, z):
    # Find d such that e*d + z*y = gcd(e,z) = 1
    
    # Calculate all our intermediate values
    a, b, u = 0, z, 1
    while(e > 0):
        q = b // e
        e, a, b, u = b % e, u, e, a - q*u

    # Make sure e and z were coprime
    if(b != 1):
        raise ValueError("invalid parameters 'e' and 'z' not coprime")
    
    d = a % z
    
    # Make sure d is positive by adding z
    while(d < 0):
        d += z

    return d
        
#=========================================================================================#
# Fuction: is_prime(num)                                                                  #
#    - num : an integer                                                                   #
# Returns True if num is prime, False otherwise                                           #
#=========================================================================================#
def is_prime (num):
    if num > 1: 
      
        # Iterate from 2 to n / 2  
       for i in range(2, num//2): 
         
           # If num is divisible by any number between  
           # 2 and n / 2, it is not prime  
           if (num % i) == 0: 
               return False 
               break
           else: 
               return True 
  
    else: 
        return False

#=========================================================================================#
# Fuction: generate_keypair(p, q)                                                         #
#    - p : a large prime integer                                                          #
#    - q : a large prime integer                                                          #
# Returns tuples containing the corresponding RSA keypairs                                #
#=========================================================================================#
def generate_keypair(p, q):
    # Check to make sure we have valid parameters (both prime, not identical)
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    
    # Always attained by multiplying (p-1) and (q-1) values
    z = (p-1) * (q-1)

    # Must be coprime of z between 1 and z (grab first, doesn't need to be random)
    e = 2
    while(e < z):
        if(gcd(e, z) == 1):
            break
        else:
            e += 1

    # Always attained by multiplying initial p and q values
    n = p * q

    # Use the dedicated function
    d = get_d(e, z)

    return ((e, n), (d, n))

#=========================================================================================#
# Fuction: encrypt(pk, plaintext)                                                         #
#    - pk        : a tuple RSA private key (e, n)                                         #
#    - plaintext : a single character of data to encrypt (string)                         #
# Returns ciphertext as decimal integer                                                   #
#=========================================================================================#
def encrypt(pk, plaintext):
    # Unpack our private key tuple into its components
    e, n = pk

    # Convert string char into 
    plaintext = ord(plaintext)

    # Apply our exponent and modulus
    cipher = pow(plaintext, e, n)

    return cipher

#=========================================================================================#
# Fuction: decrypt(pk, ciphertext)                                                        #
#    - pk         : a tuple RSA private key (e, n)                                        #
#    - ciphertext : integer representing data encrypted with the matching RSA key         #
# Returns plaintext as a single character                                                 #
#=========================================================================================#
def decrypt(pk, ciphertext):
    # Unpack our private key tuple into its components
    d, n = pk

    print(ciphertext, end='')

    # Apply our exponent and modulus
    plain = pow(ciphertext, d, n)

    # Convert back to character
    return chr(plain)