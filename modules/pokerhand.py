import numpy as np
import pandas as pd

class PokerHand:
    """
    Class that represent the poker hand
    
    Attributes
    ----------
    
    string: string
        string representation of the hand initialized with the input
    
    rank : int
        main score of the hand , based on the poker rules (1 higher, 10 lower) initialized with None
    
    array: list
        sorted numbers by repetition (main fact) and size (second fact) initialized with None
    
    Methods
    -------
    
    get_rank()
        return the rank of the hand
        
    get_array()
        return a list of sorted nubmers by repetition/frequency (main fact) and size (second fact)
    
    get_string()
        return the string representation of the hand
    
    compare_with(pokerhand_object)
        makes a comparation between the current pokerhand and the moethod argument pokerhand
        
    main_ranker(pokerhand_string)
        return rank of the poker hand
    
    HN_algorithm(hand_matrix)
        return a list of sorted nubmers by repetition/frequency (main fact) and size (second fact)
    
    """
    def __init__(self, string):
        
        self.string=string
        self.rank=None
        self.array=None
    
    def compare_with(self, pokerhand_object):
        
        self_pokerhan_rank = self.get_rank()
        another_pokerhand_rank = pokerhand_object.get_rank()
        
        
        if self_pokerhan_rank == another_pokerhand_rank:
            
                self_numbers_list=self.get_array()
                another_numbers_list=pokerhand_object.get_array()
                
                for i in range(0,len(self_numbers_list)):
                    if self_numbers_list[i] == another_numbers_list[i]:
                        pass
                    else:
                        if self_numbers_list[i] > another_numbers_list[i]:
                            result=True
                        else:
                            result=False
                        
                        break
                
        else:
                if self_pokerhan_rank < another_pokerhand_rank:
                    result=True
                else:
                    result=False
        
        
        return result
    
    def get_string(self):
        
        return self.string
    
    def get_rank(self):
        """
        
        Returns
        -------
        
        int
            return the rank of the hand
        
        """
        
        if self.rank == None:
            self.rank = self.main_ranker(self.string)
        
        return self.rank
    
    def get_array(self):
        """
        
        Returns
        -------   
        
        list
            return a list of sorted numbers by repetition/frequency (main fact) and size (second fact)
        
        """
        
        if self.array == None:
            self.array = self.HN_algorithm(self._string2matrix(self.string))
        
        return self.array
    
    def main_ranker(self,pokerhand_string):
        """
        Main function that determines the rank of the hand

        Parameters
        ----------
        pokerhand_string: string
            representation of the hand (5 cards) where each card represented by a two length string 
            and a blanck space separation between every card

        Returns
        -------
        int
            rank number

        """
        hand_matrix=self._string2matrix(pokerhand_string)
                
        numbers_frequency=hand_matrix.sum(axis=1)
        suits_frequency=hand_matrix.sum(axis=0)

        key='subspace'

        if self._check_S(numbers_frequency):
            key=key+'HS'

        if self._check_RS(suits_frequency):
            key=key+'RS'
        
        ranker={'subspace':self._sub_ranker_RN(numbers_frequency),'subspaceRS':5,'subspaceHS':6,'subspaceHSRS':self._sub_ranker_top(numbers_frequency)}

        return ranker[key]
        
    def _string2matrix(self,pokerhand_string):
        """
        Function to express the poker hand string to a poker hand matrix

        Parameters
        ----------
        pokerhand_string: string
            representation of the hand (5 cards) where each card represented by a two length string
            and a blanck space separation between every card

        Returns
        -------
        pandas dataframe
            matrix (13x4) that contains the cards position of the hand . Where the rows represents all 
            the numbers (2 to 14) and the columns represents the number of suits (C,H,S,D).

        """
        assert len(pokerhand_string)==14

        hand_matrix=pd.DataFrame(np.zeros([13,4],dtype=int),columns=['H','S','C','D'],index=list(range(2,15)))

        cards_list_string=pokerhand_string.split()

        for i in cards_list_string:
            hand_matrix.loc[self._converter(i[0]),i[1]]=1

        return hand_matrix
    
    def _converter(self,string_representation):
        """
        Auxiliar function to convert the numbers of the poker card string to integers datatype

        Parameters
        ----------
        
        string_representation : string
            card number string representation
        
        Returns
        -------
        
        int 
            also the values like J,Q,K and A have their correspondent integer representation 

        """
        assert len(string_representation) == 1

        hash_dic = {'T':10,'J':11,'Q':12,'K':13,'A':14}

        try:
            integer_representation=int(string_representation)
        except:
            integer_representation=hash_dic[string_representation]

        return integer_representation
    
    def _check_RS(self,suits_frequency):
        """
        Function that checks if the hand poker has Repeated Suits(RS)

        Parameters
        ----------
        
        suits_frequency : pandas series
            frequencies of card suits with index as the card suits

        Returns
        -------
        int
            {0,1} negative of positive respectively
        
        """
        if len(np.array(suits_frequency.loc[suits_frequency==5])) == 1:
            RS=1
        else:
            RS=0

        return RS
    
    def _check_S(self,numbers_frequency):
        """
        S:Sequence
        
        Function that checks if the hand poker has a Sequence(S)
    
        Parameters
        ----------
        
        numbers_frequency : pandas series
            frequencies of card numbers with index as the card numbers

        Returns
        -------
        int
            {0,1} negative of positive respectively

        """
        have_sequence=0
        if (len(numbers_frequency.loc[numbers_frequency==1]) == 5):
            for k in list(range(0,9)):
                if sum(numbers_frequency[k:k+5]) == 5 :
                    have_sequence=1
                    break

        return have_sequence
    
    def _sub_ranker_top(self,numbers_frequency):
        """
        Function to determine if the hand has rank 1 or 2 , after it have been being classified as 
        'Repeated Suits' and 'Sequence'
        
        Parameters
        ----------
        
        numbers_frequency : pandas series
            frequencies of card numbers with index as the card numbers

        Returns
        -------
        int
            rank number
        
        """
        rank=2

        if max(numbers_frequency.loc[numbers_frequency>0].index) == 14:
            rank=1

        return rank
    
    def _sub_ranker_RN(self,numbers_frequency):
        """
        RN=Repeated Numbers

        Function to determine the kind of RN that have the hand and assign the correspondent rank
        
        Parameters
        ----------
        
        numbers_frequency : pandas series
            frequencies of card numbers with index as the card numbers

        Returns
        -------
        int
            rank number
            
        """
        rank_dictionary={'42':3,'32':4,'33':7,'23':8,'24':9,'15':10}

        #in this subspace where sequences(of 5 cards) and repetead suits (of 5 cards) are not posible
        #there is a relation  between , max frequency  and number of different numbers (freq>0) with the rank

        case=str(max(numbers_frequency))+str(len(numbers_frequency.loc[numbers_frequency>0]))

        return rank_dictionary[case]
    
    def HN_algorithm(self,hand_matrix):
        """
        HN=High Numbers

        function that produce the array numbers to determine winner if main ranks are the same 
        
        Parameters
        ----------
        
        hand_matrix : pandas dataframe
            frequencies of card numbers with index as the card numbers

        Returns
        -------
        list 
            sorted numbers by repetition/frequency (main fact) and size (second fact)
        
        """
        numbers_frequency=hand_matrix.sum(axis=1)
        
        sorted_numbers=[]

        for i in range(1,5):
            sorted_numbers.extend(sorted(numbers_frequency.loc[numbers_frequency==(5-i)].index,reverse=True))

        return sorted_numbers